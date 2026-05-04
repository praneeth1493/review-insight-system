"""Sentiment analysis using a transformer model with a rule-based fallback."""
from __future__ import annotations

import pandas as pd
from transformers import pipeline
from tqdm import tqdm

# Lazy-loaded pipeline
_PIPELINE = None


def _get_pipeline():
    global _PIPELINE
    if _PIPELINE is None:
        print("Loading sentiment model (distilbert)...")
        _PIPELINE = pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english",
            truncation=True,
            max_length=512,
        )
    return _PIPELINE


def _map_label(label: str, score: float) -> tuple[str, float]:
    """Normalize transformer output to positive/negative/neutral."""
    label = label.upper()
    if label == "POSITIVE":
        return ("positive", score) if score >= 0.65 else ("neutral", score)
    else:
        return ("negative", score) if score >= 0.65 else ("neutral", score)


def analyze_sentiment_batch(texts: list[str], batch_size: int = 32) -> list[dict]:
    """Run sentiment analysis on a list of texts."""
    pipe = _get_pipeline()
    results = []
    for i in tqdm(range(0, len(texts), batch_size), desc="Sentiment analysis"):
        batch = texts[i : i + batch_size]
        outputs = pipe(batch)
        for out in outputs:
            sentiment, score = _map_label(out["label"], out["score"])
            results.append({"sentiment": sentiment, "confidence": round(out["score"], 4)})
    return results


# def add_sentiment(df: pd.DataFrame, text_col: str = "text") -> pd.DataFrame:
#     """Append sentiment and confidence columns to the dataframe."""
#     df = df.copy()
#     results = analyze_sentiment_batch(df[text_col].tolist())
#     df["predicted_sentiment"] = [r["sentiment"] for r in results]
#     df["sentiment_confidence"] = [r["confidence"] for r in results]
#     return df

def add_sentiment(df):
    print("Forcing TRANSFORMER model...")

    pipe = _get_pipeline()  # no try/except

    # texts = df['review'].astype(str).tolist()
    texts = df['text'].astype(str).tolist()
    

    results = pipe(texts)

    # df['sentiment'] = [r['label'].lower() for r in results]
    # df['confidence'] = [r['score'] for r in results]
    df['predicted_sentiment'] = [r['label'].lower() for r in results]
    df['sentiment_confidence'] = [r['score'] for r in results]

    return df