#!/bin/bash
# Install Python dependencies
pip install -r requirements.txt

# Download NLTK data
python -c "
import nltk
nltk.download('vader_lexicon', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)
print('NLTK data downloaded.')
"

# Generate processed data
python main.py --no-dashboard
echo "Data pipeline complete."
