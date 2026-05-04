"""Model evaluation: accuracy, precision, recall, F1-score."""
from __future__ import annotations

import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)


def _normalize_label(label: str) -> str:
    label = str(label).lower().strip()
    if label in {"positive", "pos", "5", "4"}:
        return "positive"
    if label in {"negative", "neg", "1", "2"}:
        return "negative"
    return "neutral"


def evaluate(df: pd.DataFrame, true_col: str = "label", pred_col: str = "predicted_sentiment") -> dict:
    """Compute classification metrics comparing true vs predicted labels."""
    y_true = df[true_col].apply(_normalize_label)
    y_pred = df[pred_col].apply(_normalize_label)

    labels = ["positive", "neutral", "negative"]
    present_labels = sorted(set(y_true) | set(y_pred))

    metrics = {
        "accuracy": round(accuracy_score(y_true, y_pred), 4),
        "precision_macro": round(precision_score(y_true, y_pred, average="macro", zero_division=0, labels=present_labels), 4),
        "recall_macro": round(recall_score(y_true, y_pred, average="macro", zero_division=0, labels=present_labels), 4),
        "f1_macro": round(f1_score(y_true, y_pred, average="macro", zero_division=0, labels=present_labels), 4),
        "f1_weighted": round(f1_score(y_true, y_pred, average="weighted", zero_division=0, labels=present_labels), 4),
        "per_class": {},
        "confusion_matrix": confusion_matrix(y_true, y_pred, labels=present_labels).tolist(),
        "confusion_labels": present_labels,
    }

    report = classification_report(y_true, y_pred, output_dict=True, zero_division=0, labels=present_labels)
    for label in present_labels:
        if label in report:
            metrics["per_class"][label] = {
                "precision": round(report[label]["precision"], 4),
                "recall": round(report[label]["recall"], 4),
                "f1": round(report[label]["f1-score"], 4),
                "support": int(report[label]["support"]),
            }

    return metrics


def print_evaluation_report(metrics: dict) -> None:
    """Pretty-print evaluation metrics to console."""
    print("\n" + "=" * 55)
    print("  MODEL EVALUATION REPORT")
    print("=" * 55)
    print(f"  Accuracy        : {metrics['accuracy']:.4f}")
    print(f"  Precision (macro): {metrics['precision_macro']:.4f}")
    print(f"  Recall (macro)  : {metrics['recall_macro']:.4f}")
    print(f"  F1 (macro)      : {metrics['f1_macro']:.4f}")
    print(f"  F1 (weighted)   : {metrics['f1_weighted']:.4f}")
    print("-" * 55)
    print("  Per-Class Metrics:")
    for label, m in metrics["per_class"].items():
        print(f"    {label:<12} P={m['precision']:.3f}  R={m['recall']:.3f}  F1={m['f1']:.3f}  n={m['support']}")
    print("=" * 55)
