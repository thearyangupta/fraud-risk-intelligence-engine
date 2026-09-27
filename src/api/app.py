from contextlib import asynccontextmanager
from pathlib import Path

import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.data.split import temporal_split
from src.decision.engine import make_decision
from src.features.build import build_features
from src.models.tree_models import (
    predict_tree_probabilities,
    train_gradient_boosting,
)

DATA_PATH = Path("data/fraudTrain.csv")

model = None
history: pd.DataFrame | None = None


class TransactionRequest(BaseModel):
    cc_num: int
    trans_date_trans_time: str
    merchant: str
    category: str
    amt: float


class PredictionResponse(BaseModel):
    risk_score: float
    decision: str


@asynccontextmanager
async def lifespan(app: FastAPI):
    global model
    global history

    if not DATA_PATH.exists():
        raise RuntimeError(
            f"Dataset not found: {DATA_PATH}"
        )

    df = pd.read_csv(DATA_PATH)

    train, _, _ = temporal_split(df)

    train_features = build_features(
        train,
        split_name="train",
    )

    model = train_gradient_boosting(
        train_features
    )

    history = train.copy()

    yield

    model = None
    history = None


app = FastAPI(
    title="Fraud Risk Intelligence Engine",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
    }


@app.post(
    "/predict",
    response_model=PredictionResponse,
)
def predict(
    request: TransactionRequest,
) -> PredictionResponse:
    if model is None or history is None:
        raise HTTPException(
            status_code=503,
            detail="Model is not ready.",
        )

    if request.amt < 0:
        raise HTTPException(
            status_code=400,
            detail="Transaction amount cannot be negative.",
        )

    try:
        timestamp = pd.to_datetime(
            request.trans_date_trans_time
        )
    except (TypeError, ValueError):
        raise HTTPException(
            status_code=400,
            detail="Invalid transaction timestamp.",
        ) from None

    transaction = pd.DataFrame(
        [
            {
                "cc_num": request.cc_num,
                "trans_date_trans_time": timestamp,
                "merchant": request.merchant,
                "category": request.category,
                "amt": request.amt,
                "is_fraud": 0,
            }
        ]
    )

    customer_history = history.loc[
        history["cc_num"] == request.cc_num,
        [
            "cc_num",
            "trans_date_trans_time",
            "merchant",
            "category",
            "amt",
            "is_fraud",
        ],
    ].copy()

    feature_input = pd.concat(
        [customer_history, transaction],
        ignore_index=True,
    )

    features = build_features(
        feature_input,
        split_name="api",
    )

    current_transaction = features.iloc[[-1]]

    risk_score = float(
        predict_tree_probabilities(
            model,
            current_transaction,
        ).iloc[0]
    )

    decision = make_decision(
        risk_score
    )

    return PredictionResponse(
        risk_score=risk_score,
        decision=decision,
    )