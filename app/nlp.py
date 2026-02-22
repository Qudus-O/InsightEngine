import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Download the required lexicon (only needs to be done once)
nltk.download('vader_lexicon', quiet=True)

sia = SentimentIntensityAnalyzer()

def analyze_sentiment(text: str):
    """
    Returns a score between -1 (Very Negative) and 1 (Very Positive).
    """
    scores = sia.polarity_scores(text)
    # The 'compound' score is the best overall metric for sentiment
    return scores['compound']

def get_sentiment_label(score: float):
    if score >= 0.05:
        return "Bullish (Positive)"
    elif score <= -0.05:
        return "Bearish (Negative)"
    else:
        return "Neutral"