"""Keyword and keyphrase extraction from review text."""
from __future__ import annotations

from collections import Counter

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer


def extract_tfidf_keywords(
    texts: list[str], top_n: int = 20, ngram_range: tuple = (1, 2)
) -> list[tuple[str, float]]:
    """Extract top keywords using TF-IDF across the corpus."""
    vectorizer = TfidfVectorizer(
        ngram_range=ngram_range,
        max_features=500,
        stop_words="english",
        min_df=2,
    )
    tfidf_matrix = vectorizer.fit_transform(texts)
    scores = tfidf_matrix.mean(axis=0).A1
    vocab = vectorizer.get_feature_names_out()
    ranked = sorted(zip(vocab, scores), key=lambda x: x[1], reverse=True)
    return ranked[:top_n]


def extract_keybert_keywords(
    texts: list[str], top_n: int = 10, diversity: float = 0.5
) -> list[tuple[str, float]]:
    """Extract keywords using TF-IDF (KeyBERT alternative)."""
    # Fallback to TF-IDF when KeyBERT is not available
    return extract_tfidf_keywords(texts, top_n=top_n, ngram_range=(1, 2))


def get_frequent_terms(
    df: pd.DataFrame, sentiment_filter: str | None = None, top_n: int = 20
) -> list[tuple[str, int]]:
    """Count most frequent tokens, optionally filtered by sentiment."""
    subset = df if sentiment_filter is None else df[df["predicted_sentiment"] == sentiment_filter]
    all_tokens = [token for tokens in subset["tokens"] for token in tokens]
    return Counter(all_tokens).most_common(top_n)


def keyword_summary(df: pd.DataFrame) -> dict:
    """Return keyword summaries for each sentiment class."""
    summary = {}
    for sentiment in ["positive", "negative", "neutral"]:
        subset = df[df["predicted_sentiment"] == sentiment]
        if subset.empty:
            summary[sentiment] = []
            continue
        texts = subset["clean_text"].tolist()
        summary[sentiment] = extract_tfidf_keywords(texts, top_n=15)
    return summary
