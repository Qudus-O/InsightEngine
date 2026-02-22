from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import engine, get_db
from . import models, nlp
from scraper.engine import get_financial_headlines

# Create the tables if they don't exist (safety check)
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/analyze/{ticker}")

def analyze_and_save(ticker: str, db: Session = Depends(get_db)):
    # Scrape the headlines

    news_items = get_financial_headlines(ticker)

    # Check if news_items is a dictionary (error) or empty

    if isinstance(news_items, dict) and "error" in news_items:
        raise HTTPException(status_code=500, detail=news_items["error"])

    if not news_items:
        return {"message": f"No news found for {ticker}", "data": []}

    saved_count = 0
    results = []

    for item in news_items:
        # Double check that item is a dictionary before accessing keys

        if not isinstance(item, dict):
            continue

        existing = db.query(models.SentimentResult).filter(
            models.SentimentResult.link == item['link'],
            models.SentimentResult.ticker == item['ticker'],
            models.SentimentResult.headline == item['headline']
        ).first()

        if not existing:
            score = nlp.analyze_sentiment(item.get('headline', ''))
            label = nlp.get_sentiment_label(score)

            new_record = models.SentimentResult(
                ticker=item.get('ticker'),
                headline=item.get('headline'),
                summary=item.get('summary'),
                sentiment_score=score,
                sentiment_label=label,
                published_date=item.get('date'),
                source=item.get('source'),
                link=item.get('link')
            )
            db.add(new_record)
            saved_count += 1
            results.append({"headline": item.get('headline'), "label": label, "status": "saved"})
        else:
            results.append({"headline": item.get('headline'), "status": "already exists"})
    db.commit()
    return {"ticker": ticker.upper(), "new_articles_saved": saved_count, "details": results}

