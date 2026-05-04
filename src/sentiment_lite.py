"""Lightweight sentiment analysis using VADER (no PyTorch required)."""
from __future__ import annotations

import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

# Download VADER lexicon
try:
    nltk.download("vader_lexicon", quiet=True)
except Exception:
    pass

_ANALYZER = None


def _get_analyzer():
    global _ANALYZER
    if _ANALYZER is None:
        print("Loading VADER sentiment analyzer...")
        _ANALYZER = SentimentIntensityAnalyzer()
    return _ANALYZER


def _classify_sentiment(compound_score: float) -> tuple[str, float]:
    """Map VADER compound score to sentiment label."""
    if compound_score >= 0.25:
        return "positive", abs(compound_score)
    elif compound_score <= -0.25:
        return "negative", abs(compound_score)
    else:
        return "neutral", 1.0 - abs(compound_score)


def analyze_sentiment_batch(texts: list[str]) -> list[dict]:
    """Run sentiment analysis on a list of texts using VADER."""
    analyzer = _get_analyzer()
    results = []
    
    for text in texts:
        scores = analyzer.polarity_scores(text)
        sentiment, confidence = _classify_sentiment(scores["compound"])
        results.append({
            "sentiment": sentiment,
            "confidence": round(confidence, 4)
        })
    
    return results


def add_sentiment(df: pd.DataFrame, text_col: str = "text") -> pd.DataFrame:
    """Append sentiment and confidence columns to the dataframe."""
    df = df.copy()
    print(f"  Analyzing {len(df)} reviews...")
    results = analyze_sentiment_batch(df[text_col].tolist())
    df["predicted_sentiment"] = [r["sentiment"] for r in results]
    df["sentiment_confidence"] = [r["confidence"] for r in results]
    return df
