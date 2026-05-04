"""Insight generation: recurring problems, positive features, recommendations."""
from __future__ import annotations

from collections import defaultdict

import pandas as pd

from src.aspects import get_aspect_summary
from src.keywords import get_frequent_terms


def detect_recurring_problems(df: pd.DataFrame, min_count: int = 3) -> list[dict]:
    """Identify aspects with high negative sentiment counts."""
    neg_df = df[df["predicted_sentiment"] == "negative"]
    problem_counts: dict[str, int] = defaultdict(int)

    for aspects in neg_df["aspects"]:
        for aspect in aspects:
            problem_counts[aspect] += 1

    problems = [
        {"aspect": aspect, "complaint_count": count, "severity": _severity(count, len(neg_df))}
        for aspect, count in sorted(problem_counts.items(), key=lambda x: x[1], reverse=True)
        if count >= min_count
    ]
    return problems


def _severity(count: int, total: int) -> str:
    ratio = count / max(total, 1)
    if ratio >= 0.4:
        return "critical"
    elif ratio >= 0.2:
        return "high"
    elif ratio >= 0.1:
        return "medium"
    return "low"


def highlight_positive_features(df: pd.DataFrame, min_count: int = 3) -> list[dict]:
    """Identify aspects with high positive sentiment counts."""
    pos_df = df[df["predicted_sentiment"] == "positive"]
    feature_counts: dict[str, int] = defaultdict(int)

    for aspects in pos_df["aspects"]:
        for aspect in aspects:
            feature_counts[aspect] += 1

    return [
        {"aspect": aspect, "praise_count": count}
        for aspect, count in sorted(feature_counts.items(), key=lambda x: x[1], reverse=True)
        if count >= min_count
    ]


def generate_recommendations(df: pd.DataFrame) -> list[dict]:
    """Generate data-driven product improvement recommendations."""
    aspect_summary = get_aspect_summary(df)
    problems = detect_recurring_problems(df)
    recommendations = []

    problem_aspects = {p["aspect"]: p for p in problems}

    for _, row in aspect_summary.iterrows():
        aspect = row["aspect"]
        if aspect not in problem_aspects:
            continue

        severity = problem_aspects[aspect]["severity"]
        neg_keywords = get_frequent_terms(
            df[df["predicted_sentiment"] == "negative"], top_n=5
        )
        neg_kw_str = ", ".join([kw for kw, _ in neg_keywords[:3]])

        rec = _build_recommendation(aspect, severity, row, neg_kw_str)
        if rec:
            recommendations.append(rec)

    return recommendations


def _build_recommendation(
    aspect: str, severity: str, row: pd.Series, neg_keywords: str
) -> dict | None:
    templates = {
        "battery": "Improve battery capacity or optimize power management firmware to extend usage time.",
        "camera": "Enhance camera software algorithms and low-light performance through firmware updates.",
        "display": "Address touchscreen responsiveness issues and improve display calibration.",
        "performance": "Optimize software and reduce background processes to improve device speed and stability.",
        "build_quality": "Review materials and manufacturing QC to reduce fragility and defect rates.",
        "software": "Prioritize bug fixes and stability improvements in the next software release.",
        "audio": "Improve speaker tuning and microphone noise cancellation in firmware.",
        "connectivity": "Investigate and fix Bluetooth/WiFi driver issues causing frequent disconnections.",
        "customer_service": "Invest in customer support training and streamline the warranty/return process.",
        "value": "Reassess pricing strategy or enhance feature set to better match customer expectations.",
        "design": "Conduct ergonomic review and consider design improvements based on user feedback.",
        "delivery": "Improve packaging standards and partner with more reliable shipping carriers.",
        "general": "Conduct a comprehensive product review based on customer feedback patterns.",
    }
    action = templates.get(aspect, templates["general"])
    return {
        "aspect": aspect,
        "severity": severity,
        "negative_count": int(row.get("negative", 0)),
        "positive_count": int(row.get("positive", 0)),
        "recommendation": action,
        "related_keywords": neg_keywords,
    }


def generate_full_report(df: pd.DataFrame) -> dict:
    """Compile a complete insight report."""
    total = len(df)
    sentiment_dist = df["predicted_sentiment"].value_counts().to_dict()
    avg_confidence = df["sentiment_confidence"].mean()

    return {
        "total_reviews": total,
        "sentiment_distribution": sentiment_dist,
        "average_confidence": round(avg_confidence, 4),
        "recurring_problems": detect_recurring_problems(df),
        "positive_features": highlight_positive_features(df),
        "recommendations": generate_recommendations(df),
        "aspect_summary": get_aspect_summary(df).to_dict(orient="records"),
    }
