"""Flask API — serves processed review data to the React frontend."""
import ast
import json
import os
import sys
from collections import Counter

import nltk
import pandas as pd
from flask import Flask, jsonify, request

# Download NLTK data on startup
for pkg in ["vader_lexicon", "stopwords", "wordnet", "punkt"]:
    try:
        nltk.download(pkg, quiet=True)
    except Exception:
        pass

# Allow imports from src/
sys.path.insert(0, os.path.dirname(__file__))

app = Flask(__name__)


# ── CORS ────────────────────────────────────────────────────────────────────
@app.after_request
def add_cors(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response


# ── Data loading ─────────────────────────────────────────────────────────────
def _load():
    base = os.path.dirname(__file__)
    csv_path  = os.path.join(base, "processed_reviews.csv")
    json_path = os.path.join(base, "report.json")

    df = pd.read_csv(csv_path)
    df["tokens"]           = df["tokens"].apply(ast.literal_eval)
    df["aspects"]          = df["aspects"].apply(ast.literal_eval)
    df["aspect_sentiments"]= df["aspect_sentiments"].apply(ast.literal_eval)

    with open(json_path) as f:
        report = json.load(f)
    return df, report


DF, REPORT = _load()


# ── Endpoints ────────────────────────────────────────────────────────────────
@app.route("/api/summary", methods=["GET"])
def summary():
    total = REPORT["total_reviews"]
    dist  = REPORT["sentiment_distribution"]
    pos   = dist.get("positive", 0)
    neg   = dist.get("negative", 0)
    neu   = dist.get("neutral",  0)
    return jsonify({
        "total_reviews":  total,
        "positive":       pos,
        "negative":       neg,
        "neutral":        neu,
        "positive_pct":   round(pos / total * 100, 1),
        "negative_pct":   round(neg / total * 100, 1),
        "neutral_pct":    round(neu / total * 100, 1),
        "avg_confidence": REPORT["average_confidence"],
    })


@app.route("/api/sentiment-distribution", methods=["GET"])
def sentiment_distribution():
    dist = REPORT["sentiment_distribution"]
    return jsonify([
        {"label": k.capitalize(), "value": v, "key": k}
        for k, v in dist.items()
    ])


@app.route("/api/aspect-summary", methods=["GET"])
def aspect_summary():
    return jsonify(REPORT["aspect_summary"])


@app.route("/api/problems", methods=["GET"])
def problems():
    return jsonify(REPORT["recurring_problems"])


@app.route("/api/positive-features", methods=["GET"])
def positive_features():
    return jsonify(REPORT["positive_features"])


@app.route("/api/recommendations", methods=["GET"])
def recommendations():
    return jsonify(REPORT["recommendations"])


@app.route("/api/keywords", methods=["GET"])
def keywords():
    result = {}
    for sentiment in ["positive", "negative", "neutral"]:
        subset     = DF[DF["predicted_sentiment"] == sentiment]
        all_tokens = [t for tokens in subset["tokens"] for t in tokens]
        top        = Counter(all_tokens).most_common(20)
        result[sentiment] = [{"word": w, "count": c} for w, c in top]
    return jsonify(result)


@app.route("/api/reviews", methods=["GET"])
def reviews():
    page      = int(request.args.get("page", 1))
    per_page  = int(request.args.get("per_page", 10))
    sentiment = request.args.get("sentiment", None)
    subset    = DF if not sentiment else DF[DF["predicted_sentiment"] == sentiment]
    total     = len(subset)
    start     = (page - 1) * per_page
    end       = start + per_page
    cols      = ["review_id", "text", "rating", "predicted_sentiment",
                 "sentiment_confidence", "aspects"]
    rows      = subset.iloc[start:end][cols].copy()
    rows["aspects"] = rows["aspects"].apply(lambda x: x if isinstance(x, list) else [])
    return jsonify({
        "total":    total,
        "page":     page,
        "per_page": per_page,
        "reviews":  rows.to_dict(orient="records"),
    })


@app.route("/api/metrics", methods=["GET"])
def metrics():
    from src.evaluator import evaluate
    m = evaluate(DF)
    return jsonify(m)


@app.route("/api/analyze", methods=["POST", "OPTIONS"])
def analyze_single():
    if request.method == "OPTIONS":
        return jsonify({}), 200
    body = request.get_json(force=True)
    text = body.get("text", "").strip()
    if not text:
        return jsonify({"error": "No text provided"}), 400

    from src.preprocessor      import tokenize_and_lemmatize
    from src.sentiment_lite    import analyze_sentiment_batch
    from src.aspects           import _detect_aspects, _aspect_sentiment

    tokens           = tokenize_and_lemmatize(text)
    sentiment_result = analyze_sentiment_batch([text])[0]
    aspects          = _detect_aspects(text)
    aspect_sentiments= {a: _aspect_sentiment(text, a) for a in aspects}

    return jsonify({
        "text":              text,
        "sentiment":         sentiment_result["sentiment"],
        "confidence":        sentiment_result["confidence"],
        "aspects":           aspects,
        "aspect_sentiments": aspect_sentiments,
        "keywords":          tokens[:10],
    })


if __name__ == "__main__":
    print("API running at http://localhost:5000")
    app.run(debug=False, port=5000)
