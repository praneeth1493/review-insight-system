"""
Review Insight System — Entry Point
Usage:
    python main.py                  # Run full pipeline + launch dashboard
    python main.py --no-dashboard   # Run pipeline only, print report
    python main.py --csv path.csv   # Use your own CSV (needs 'text' and 'label' columns)
"""
import argparse
import json
import sys

import pandas as pd

from data.sample_reviews import generate_dataset
from src.preprocessor import preprocess_dataframe
from src.sentiment_lite import add_sentiment
from src.aspects import classify_aspects
from src.keywords import keyword_summary
from src.insights import generate_full_report
from src.evaluator import evaluate, print_evaluation_report
# dashboard not needed for API deployment
# from src.dashboard import build_app


def load_data(csv_path: str | None, n_samples: int = 300) -> pd.DataFrame:
    if csv_path:
        print(f"Loading data from {csv_path}...")
        df = pd.read_csv(csv_path)
        required = {"text"}
        if not required.issubset(df.columns):
            print(f"ERROR: CSV must contain columns: {required}")
            sys.exit(1)
        if "label" not in df.columns:
            print("Warning: No 'label' column found — evaluation metrics will be skipped.")
    else:
        print(f"Generating {n_samples} sample reviews...")
        df = generate_dataset(n_samples)
    return df


def run_pipeline(df: pd.DataFrame) -> tuple[pd.DataFrame, dict, dict]:
    print("\n[1/5] Preprocessing text...")
    df = preprocess_dataframe(df)

    print("[2/5] Running sentiment analysis...")
    df = add_sentiment(df)

    print("[3/5] Classifying aspects...")
    df = classify_aspects(df)

    print("[4/5] Generating insights...")
    report = generate_full_report(df)

    print("[5/5] Evaluating model...")
    metrics = {}
    if "label" in df.columns:
        metrics = evaluate(df)
        print_evaluation_report(metrics)
    else:
        print("  Skipped (no ground-truth labels).")

    return df, report, metrics


def print_insights(report: dict) -> None:
    print("\n" + "=" * 55)
    print("  INSIGHT REPORT SUMMARY")
    print("=" * 55)
    print(f"  Total Reviews : {report['total_reviews']}")
    print(f"  Sentiment     : {report['sentiment_distribution']}")
    print(f"  Avg Confidence: {report['average_confidence']}")

    print("\n  Top Recurring Problems:")
    for p in report["recurring_problems"][:5]:
        print(f"    [{p['severity'].upper():8}] {p['aspect']:<20} ({p['complaint_count']} complaints)")

    print("\n  Top Positive Features:")
    for f in report["positive_features"][:5]:
        print(f"    {f['aspect']:<20} ({f['praise_count']} mentions)")

    print("\n  Recommendations:")
    for r in report["recommendations"][:5]:
        print(f"    [{r['severity'].upper():8}] {r['aspect']}: {r['recommendation']}")
    print("=" * 55)


def main():
    parser = argparse.ArgumentParser(description="Customer Review Insight System")
    parser.add_argument("--csv", type=str, default=None, help="Path to CSV file with reviews")
    parser.add_argument("--samples", type=int, default=300, help="Number of sample reviews to generate")
    parser.add_argument("--no-dashboard", action="store_true", help="Skip launching the dashboard")
    parser.add_argument("--port", type=int, default=8050, help="Dashboard port (default: 8050)")
    args = parser.parse_args()

    df = load_data(args.csv, args.samples)
    df, report, metrics = run_pipeline(df)
    print_insights(report)

    # Save processed data
    df.to_csv("processed_reviews.csv", index=False)
    with open("report.json", "w") as f:
        json.dump(report, f, indent=2, default=str)
    print("\nSaved: processed_reviews.csv, report.json")

    if not args.no_dashboard:
        print("Dashboard not available in API-only mode.")
        print("Use the React frontend instead: npm run dev")


if __name__ == "__main__":
    main()
