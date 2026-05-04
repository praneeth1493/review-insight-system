"""Flask API — serves processed review data to the React frontend."""
import ast
import json
import os
import sys
from collections import Counter

import nltk
import pandas as pd
from flask import Flask, jsonify, request
from flask.wrappers import Response

# Download NLTK data on startup (needed for deployment)
for pkg in ["vader_lexicon", "stopwords", "wordnet", "punkt", "punkt_tab"]:
    try:
        nltk.download(pkg, quiet=True)
    except Exception:
        pass

# Allow imports from src/
sys.path.insert(0, os.path.dirname(__file__))

app = Flask(__name__)

# ── CORS (allow React dev server) ──────────────────────────────────────────
@app.after_request
def add_cors(response: Response) -> Response:
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response


# ── Data loading ────────────────────────────────────────────────────────────
def _load():
    base = os.path.dirname(__file__)
    csv_path = os.path.join(base, "processed_reviews.csv")
    report_path = os.path.join(base, "report.json")

    # Auto-generate data if not present (first deploy)
    if not os.path.exists(csv_path) or not os.path.exists(report_path):
        print("Data files not found — running pipeline to generate them...")
        from data.sample_reviews import generate_dataset
        from src.preprocessor import preprocess_dataframe
        from src.sentiment_lite import add_sentiment
        from src.aspects import classify_aspects
        from src.insights import generate_full_report
        import json as _json

        df = generate_dataset(300)
        df = preprocess_dataframe(df)
        df = add_sentiment(df)
        df = classify_aspects(df)
        report = generate_full_report(df)
        df.to_csv(csv_path, index=False)
        with open(report_path, "w") as f:
            _json.dump(report, f, indent=2, default=str)
        print("Data generated successfully.")

    df = pd.read_csv(csv_path)
    df["tokens"] = df["tokens"].apply(ast.literal_eval)
    df["aspects"] = df["aspects"].apply(ast.literal_eval)
    df["aspect_sentiments"] = df["aspect_sentiments"].apply(ast.literal_eval)
    with open(report_path) as f:
        report = json.load(f)
    return df, report


DF, REPORT = _load()


# ── Endpoints ───────────────────────────────────────────────────────────────
@app.get("/api/summary")
def summary():
    total = REPORT["total_reviews"]
    dist = REPORT["sentiment_distribution"]
    pos = dist.get("positive", 0)
    neg = dist.get("negative", 0)
    neu = dist.get("neutral", 0)
    return jsonify({
        "total_reviews": total,
        "positive": pos,
        "negative": neg,
        "neutral": neu,
        "positive_pct": round(pos / total * 100, 1),
        "negative_pct": round(neg / total * 100, 1),
        "neutral_pct": round(neu / total * 100, 1),
        "avg_confidence": REPORT["average_confidence"],
    })


@app.get("/api/sentiment-distribution")
def sentiment_distribution():
    dist = REPORT["sentiment_distribution"]
    return jsonify([
        {"label": k.capitalize(), "value": v, "key": k}
        for k, v in dist.items()
    ])


@app.get("/api/aspect-summary")
def aspect_summary():
    return jsonify(REPORT["aspect_summary"])


@app.get("/api/problems")
def problems():
    return jsonify(REPORT["recurring_problems"])


@app.get("/api/positive-features")
def positive_features():
    return jsonify(REPORT["positive_features"])


@app.get("/api/recommendations")
def recommendations():
    return jsonify(REPORT["recommendations"])


@app.get("/api/keywords")
def keywords():
    result = {}
    for sentiment in ["positive", "negative", "neutral"]:
        subset = DF[DF["predicted_sentiment"] == sentiment]
        all_tokens = [t for tokens in subset["tokens"] for t in tokens]
        top = Counter(all_tokens).most_common(20)
        result[sentiment] = [{"word": w, "count": c} for w, c in top]
    return jsonify(result)


@app.get("/api/reviews")
def reviews():
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))
    sentiment = request.args.get("sentiment", None)
    subset = DF if not sentiment else DF[DF["predicted_sentiment"] == sentiment]
    total = len(subset)
    start = (page - 1) * per_page
    end = start + per_page
    rows = subset.iloc[start:end][["review_id", "text", "rating", "predicted_sentiment",
                                    "sentiment_confidence", "aspects"]].copy()
    rows["aspects"] = rows["aspects"].apply(lambda x: x if isinstance(x, list) else [])
    return jsonify({
        "total": total,
        "page": page,
        "per_page": per_page,
        "reviews": rows.to_dict(orient="records"),
    })


@app.get("/api/metrics")
def metrics():
    from src.evaluator import evaluate
    m = evaluate(DF)
    return jsonify(m)


@app.post("/api/analyze")
def analyze_single():
    """Analyze a single review text submitted from the frontend."""
    body = request.get_json(force=True)
    text = body.get("text", "").strip()
    if not text:
        return jsonify({"error": "No text provided"}), 400

    from src.preprocessor import tokenize_and_lemmatize
    from src.sentiment_lite import analyze_sentiment_batch
    from src.aspects import _detect_aspects, _aspect_sentiment

    tokens = tokenize_and_lemmatize(text)
    sentiment_result = analyze_sentiment_batch([text])[0]
    aspects = _detect_aspects(text)
    aspect_sentiments = {a: _aspect_sentiment(text, a) for a in aspects}

    return jsonify({
        "text": text,
        "sentiment": sentiment_result["sentiment"],
        "confidence": sentiment_result["confidence"],
        "aspects": aspects,
        "aspect_sentiments": aspect_sentiments,
        "keywords": tokens[:10],
    })


if __name__ == "__main__":
    print("API running at http://localhost:5000")
    app.run(debug=False, port=5000)
