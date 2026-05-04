"""Interactive Dash dashboard for review insights visualization."""
from __future__ import annotations

import json

import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Input, Output, dcc, html

from src.aspects import get_aspect_summary
from src.keywords import get_frequent_terms


def _sentiment_pie(df: pd.DataFrame) -> go.Figure:
    counts = df["predicted_sentiment"].value_counts().reset_index()
    counts.columns = ["sentiment", "count"]
    color_map = {"positive": "#2ecc71", "neutral": "#f39c12", "negative": "#e74c3c"}
    fig = px.pie(
        counts, names="sentiment", values="count",
        color="sentiment", color_discrete_map=color_map,
        title="Sentiment Distribution",
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    fig.update_layout(showlegend=False, margin=dict(t=50, b=10, l=10, r=10))
    return fig


def _aspect_bar(df: pd.DataFrame) -> go.Figure:
    summary = get_aspect_summary(df)
    fig = go.Figure()
    for sentiment, color in [("positive", "#2ecc71"), ("neutral", "#f39c12"), ("negative", "#e74c3c")]:
        if sentiment in summary.columns:
            fig.add_trace(go.Bar(
                name=sentiment.capitalize(),
                x=summary["aspect"],
                y=summary[sentiment],
                marker_color=color,
            ))
    fig.update_layout(
        barmode="stack",
        title="Aspect-Based Sentiment Breakdown",
        xaxis_title="Aspect",
        yaxis_title="Review Count",
        legend_title="Sentiment",
        margin=dict(t=50, b=80, l=40, r=10),
        xaxis_tickangle=-30,
    )
    return fig


def _top_complaints_bar(df: pd.DataFrame) -> go.Figure:
    terms = get_frequent_terms(df, sentiment_filter="negative", top_n=15)
    words, counts = zip(*terms) if terms else ([], [])
    fig = px.bar(
        x=list(counts), y=list(words),
        orientation="h",
        title="Top Complaint Keywords",
        labels={"x": "Frequency", "y": "Keyword"},
        color=list(counts),
        color_continuous_scale="Reds",
    )
    fig.update_layout(
        yaxis=dict(autorange="reversed"),
        coloraxis_showscale=False,
        margin=dict(t=50, b=10, l=10, r=10),
    )
    return fig


def _top_praise_bar(df: pd.DataFrame) -> go.Figure:
    terms = get_frequent_terms(df, sentiment_filter="positive", top_n=15)
    words, counts = zip(*terms) if terms else ([], [])
    fig = px.bar(
        x=list(counts), y=list(words),
        orientation="h",
        title="Top Positive Keywords",
        labels={"x": "Frequency", "y": "Keyword"},
        color=list(counts),
        color_continuous_scale="Greens",
    )
    fig.update_layout(
        yaxis=dict(autorange="reversed"),
        coloraxis_showscale=False,
        margin=dict(t=50, b=10, l=10, r=10),
    )
    return fig


def _confidence_histogram(df: pd.DataFrame) -> go.Figure:
    fig = px.histogram(
        df, x="sentiment_confidence", color="predicted_sentiment",
        nbins=20,
        title="Sentiment Confidence Distribution",
        color_discrete_map={"positive": "#2ecc71", "neutral": "#f39c12", "negative": "#e74c3c"},
        labels={"sentiment_confidence": "Confidence Score", "count": "Reviews"},
    )
    fig.update_layout(barmode="overlay", margin=dict(t=50, b=10, l=10, r=10))
    fig.update_traces(opacity=0.75)
    return fig


def _aspect_score_gauge(df: pd.DataFrame) -> go.Figure:
    summary = get_aspect_summary(df)
    top = summary.head(8)
    fig = px.bar(
        top, x="aspect", y="sentiment_score",
        title="Aspect Sentiment Score (-1 = all negative, +1 = all positive)",
        color="sentiment_score",
        color_continuous_scale="RdYlGn",
        range_color=[-1, 1],
    )
    fig.add_hline(y=0, line_dash="dash", line_color="gray")
    fig.update_layout(margin=dict(t=60, b=10, l=10, r=10), coloraxis_showscale=False)
    return fig


def _recommendations_table(report: dict) -> dbc.Table:
    recs = report.get("recommendations", [])
    if not recs:
        return html.P("No recommendations generated.", className="text-muted")

    severity_badge = {
        "critical": "danger", "high": "warning", "medium": "info", "low": "secondary"
    }
    rows = []
    for r in recs:
        badge_color = severity_badge.get(r["severity"], "secondary")
        rows.append(html.Tr([
            html.Td(r["aspect"].replace("_", " ").title()),
            html.Td(dbc.Badge(r["severity"].upper(), color=badge_color, className="me-1")),
            html.Td(r["negative_count"]),
            html.Td(r["recommendation"]),
        ]))

    return dbc.Table(
        [
            html.Thead(html.Tr([
                html.Th("Aspect"), html.Th("Severity"),
                html.Th("Complaints"), html.Th("Recommendation"),
            ])),
            html.Tbody(rows),
        ],
        bordered=True, hover=True, responsive=True, striped=True, size="sm",
    )


def build_app(df: pd.DataFrame, report: dict, metrics: dict) -> dash.Dash:
    """Build and return the Dash application."""
    app = dash.Dash(
        __name__,
        external_stylesheets=[dbc.themes.FLATLY],
        title="Review Insight Dashboard",
    )

    total = report["total_reviews"]
    pos_pct = round(report["sentiment_distribution"].get("positive", 0) / total * 100, 1)
    neg_pct = round(report["sentiment_distribution"].get("negative", 0) / total * 100, 1)
    neu_pct = round(report["sentiment_distribution"].get("neutral", 0) / total * 100, 1)

    app.layout = dbc.Container(fluid=True, children=[
        # Header
        dbc.Row(dbc.Col(html.H2(
            "Customer Review Intelligence Dashboard",
            className="text-center text-white bg-primary p-3 rounded mt-3 mb-4",
        ))),

        # KPI Cards
        dbc.Row([
            dbc.Col(dbc.Card([dbc.CardBody([
                html.H4(total, className="card-title text-center"),
                html.P("Total Reviews", className="card-text text-center text-muted"),
            ])], color="light"), width=3),
            dbc.Col(dbc.Card([dbc.CardBody([
                html.H4(f"{pos_pct}%", className="card-title text-center text-success"),
                html.P("Positive", className="card-text text-center text-muted"),
            ])], color="light"), width=3),
            dbc.Col(dbc.Card([dbc.CardBody([
                html.H4(f"{neg_pct}%", className="card-title text-center text-danger"),
                html.P("Negative", className="card-text text-center text-muted"),
            ])], color="light"), width=3),
            dbc.Col(dbc.Card([dbc.CardBody([
                html.H4(f"{metrics['f1_macro']:.3f}", className="card-title text-center text-info"),
                html.P("F1 Score (macro)", className="card-text text-center text-muted"),
            ])], color="light"), width=3),
        ], className="mb-4"),

        # Row 1: Sentiment pie + Aspect bar
        dbc.Row([
            dbc.Col(dcc.Graph(figure=_sentiment_pie(df)), width=4),
            dbc.Col(dcc.Graph(figure=_aspect_bar(df)), width=8),
        ], className="mb-4"),

        # Row 2: Top complaints + Top praise
        dbc.Row([
            dbc.Col(dcc.Graph(figure=_top_complaints_bar(df)), width=6),
            dbc.Col(dcc.Graph(figure=_top_praise_bar(df)), width=6),
        ], className="mb-4"),

        # Row 3: Confidence histogram + Aspect score
        dbc.Row([
            dbc.Col(dcc.Graph(figure=_confidence_histogram(df)), width=6),
            dbc.Col(dcc.Graph(figure=_aspect_score_gauge(df)), width=6),
        ], className="mb-4"),

        # Evaluation Metrics
        dbc.Row(dbc.Col([
            html.H5("Model Evaluation Metrics", className="mb-3"),
            dbc.Row([
                dbc.Col(dbc.Card([dbc.CardBody([
                    html.H5(f"{metrics['accuracy']:.4f}", className="text-center"),
                    html.P("Accuracy", className="text-center text-muted mb-0"),
                ])], color="light"), width=3),
                dbc.Col(dbc.Card([dbc.CardBody([
                    html.H5(f"{metrics['precision_macro']:.4f}", className="text-center"),
                    html.P("Precision", className="text-center text-muted mb-0"),
                ])], color="light"), width=3),
                dbc.Col(dbc.Card([dbc.CardBody([
                    html.H5(f"{metrics['recall_macro']:.4f}", className="text-center"),
                    html.P("Recall", className="text-center text-muted mb-0"),
                ])], color="light"), width=3),
                dbc.Col(dbc.Card([dbc.CardBody([
                    html.H5(f"{metrics['f1_weighted']:.4f}", className="text-center"),
                    html.P("F1 Weighted", className="text-center text-muted mb-0"),
                ])], color="light"), width=3),
            ]),
        ], className="mb-4")),

        # Recommendations Table
        dbc.Row(dbc.Col([
            html.H5("Product Improvement Recommendations", className="mb-3"),
            _recommendations_table(report),
        ], className="mb-4")),

        # Footer
        dbc.Row(dbc.Col(html.P(
            "Review Insight System — Powered by DistilBERT + KeyBERT",
            className="text-center text-muted small pb-3",
        ))),
    ])

    return app
