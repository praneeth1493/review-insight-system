#!/usr/bin/env bash
set -e

echo "Python version:"
python --version

echo "==> Installing dependencies..."
pip install -r requirements.txt

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
