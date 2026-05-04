"""Aspect-based sentiment classification for product reviews."""
from __future__ import annotations

import re
import pandas as pd

# Aspect taxonomy: aspect_name -> keywords
ASPECT_TAXONOMY: dict[str, list[str]] = {
    "battery": ["battery", "charge", "charging", "power", "drain", "life", "hours"],
    "camera": ["camera", "photo", "picture", "image", "lens", "video", "shot", "blur", "focus"],
    "display": ["screen", "display", "resolution", "brightness", "color", "pixel", "touch"],
    "performance": ["speed", "fast", "slow", "lag", "performance", "processor", "ram", "freeze", "crash"],
    "build_quality": ["build", "quality", "durable", "fragile", "material", "plastic", "metal", "solid"],
    "software": ["software", "app", "update", "bug", "interface", "ui", "os", "system", "feature"],
    "audio": ["sound", "speaker", "audio", "volume", "bass", "microphone", "noise", "headphone"],
    "connectivity": ["wifi", "bluetooth", "connection", "network", "signal", "pair", "sync"],
    "customer_service": ["support", "service", "warranty", "return", "refund", "customer", "staff", "response"],
    "value": ["price", "value", "cost", "worth", "expensive", "cheap", "money", "afford"],
    "design": ["design", "look", "style", "color", "size", "weight", "slim", "compact", "ergonomic"],
    "delivery": ["delivery", "shipping", "packaging", "arrived", "box", "damage"],
}

# Sentiment signals per aspect context
POSITIVE_SIGNALS = {
    "excellent", "great", "good", "amazing", "fantastic", "love", "perfect",
    "best", "incredible", "outstanding", "superb", "impressive", "beautiful",
    "crisp", "vivid", "fast", "quick", "smooth", "reliable", "solid", "durable",
    "helpful", "easy", "intuitive", "seamless", "stunning", "phenomenal",
}
NEGATIVE_SIGNALS = {
    "bad", "terrible", "awful", "poor", "horrible", "worst", "broken", "fail",
    "slow", "crash", "bug", "issue", "problem", "defect", "disappoint", "frustrat",
    "blurry", "hot", "overheat", "drain", "short", "weak", "cheap", "fragile",
    "rude", "unhelpful", "mislead", "damage", "scratch", "stiff", "unresponsive",
}


def _detect_aspects(text: str) -> list[str]:
    """Return list of aspects mentioned in the text."""
    text_lower = text.lower()
    found = []
    for aspect, keywords in ASPECT_TAXONOMY.items():
        if any(kw in text_lower for kw in keywords):
            found.append(aspect)
    return found if found else ["general"]


def _aspect_sentiment(text: str, aspect: str) -> str:
    """Determine sentiment for a specific aspect using window-based heuristic."""
    text_lower = text.lower()
    keywords = ASPECT_TAXONOMY.get(aspect, [])

    # Find positions of aspect keywords
    positions = []
    for kw in keywords:
        for m in re.finditer(r"\b" + re.escape(kw) + r"\b", text_lower):
            positions.append(m.start())

    if not positions:
        return "neutral"

    # Check a ±60 char window around each keyword position
    pos_count, neg_count = 0, 0
    for pos in positions:
        window = text_lower[max(0, pos - 60) : pos + 60]
        for sig in POSITIVE_SIGNALS:
            if sig in window:
                pos_count += 1
        for sig in NEGATIVE_SIGNALS:
            if sig in window:
                neg_count += 1

    if pos_count > neg_count:
        return "positive"
    elif neg_count > pos_count:
        return "negative"
    return "neutral"


def classify_aspects(df: pd.DataFrame, text_col: str = "text") -> pd.DataFrame:
    """Add aspect_labels and aspect_sentiments columns to the dataframe."""
    df = df.copy()
    aspect_labels = []
    aspect_sentiments = []

    for text in df[text_col]:
        aspects = _detect_aspects(text)
        sentiments = {a: _aspect_sentiment(text, a) for a in aspects}
        aspect_labels.append(aspects)
        aspect_sentiments.append(sentiments)

    df["aspects"] = aspect_labels
    df["aspect_sentiments"] = aspect_sentiments
    return df


def get_aspect_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate aspect sentiment counts across all reviews."""
    rows = []
    for _, row in df.iterrows():
        for aspect, sentiment in row["aspect_sentiments"].items():
            rows.append({"aspect": aspect, "sentiment": sentiment})

    summary = (
        pd.DataFrame(rows)
        .groupby(["aspect", "sentiment"])
        .size()
        .reset_index(name="count")
        .pivot_table(index="aspect", columns="sentiment", values="count", fill_value=0)
        .reset_index()
    )
    # Ensure all columns exist
    for col in ["positive", "negative", "neutral"]:
        if col not in summary.columns:
            summary[col] = 0
    summary["total"] = summary[["positive", "negative", "neutral"]].sum(axis=1)
    summary["sentiment_score"] = (
        (summary["positive"] - summary["negative"]) / summary["total"]
    ).round(3)
    return summary.sort_values("total", ascending=False)
