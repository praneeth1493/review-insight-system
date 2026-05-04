#!/usr/bin/env bash
set -e

echo "==> Python version:"
python --version

echo "==> Upgrading pip..."
pip install --upgrade pip

echo "==> Installing dependencies (pre-built wheels only)..."
pip install --only-binary=:all: pandas==2.0.3 numpy==1.25.2 scikit-learn==1.3.2
pip install flask==2.3.3 Werkzeug==2.3.7 nltk==3.8.1 gunicorn==21.2.0

echo "==> Downloading NLTK data..."
python -c "
import nltk
nltk.download('vader_lexicon', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('punkt', quiet=True)
print('NLTK data ready.')
"

echo "==> Running data pipeline..."
python main.py --no-dashboard

echo "==> Build complete!"
