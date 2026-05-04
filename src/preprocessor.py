"""Text preprocessing pipeline for review data."""
import re
import string
import nltk
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

# Download required NLTK data
for resource in ["punkt", "stopwords", "wordnet", "averaged_perceptron_tagger", "punkt_tab"]:
    try:
        nltk.download(resource, quiet=True)
    except Exception:
        pass

LEMMATIZER = WordNetLemmatizer()
STOP_WORDS = set(stopwords.words("english"))
# Keep negation words — they matter for sentiment
NEGATION_WORDS = {"no", "not", "never", "neither", "nor", "none", "nobody", "nothing", "nowhere"}
STOP_WORDS -= NEGATION_WORDS


def clean_text(text: str) -> str:
    """Lowercase, remove HTML, URLs, punctuation, and extra whitespace."""
    text = str(text).lower()
    text = re.sub(r"<[^>]+>", " ", text)          # HTML tags
    text = re.sub(r"http\S+|www\S+", " ", text)   # URLs
    text = re.sub(r"[^a-z\s']", " ", text)        # keep letters and apostrophes
    text = re.sub(r"\s+", " ", text).strip()
    return text


def tokenize_and_lemmatize(text: str) -> list[str]:
    """Tokenize, remove stopwords, and lemmatize."""
    tokens = word_tokenize(clean_text(text))
    return [
        LEMMATIZER.lemmatize(t)
        for t in tokens
        if t not in STOP_WORDS and len(t) > 2
    ]


def preprocess_dataframe(df: pd.DataFrame, text_col: str = "text") -> pd.DataFrame:
    """Add cleaned and tokenized columns to the dataframe."""
    df = df.copy()
    df["clean_text"] = df[text_col].apply(clean_text)
    df["tokens"] = df["clean_text"].apply(tokenize_and_lemmatize)
    df["token_str"] = df["tokens"].apply(lambda t: " ".join(t))
    return df
