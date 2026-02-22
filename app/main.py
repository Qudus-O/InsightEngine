from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import engine, get_db
from . import models, nlp
from scraper.engine import get_financial_headlines
from datetime import datetime, timedelta

# Create the tables if they don't exist
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/analyze/{ticker}")
def analyze_and_save(ticker: str, db: Session = Depends(get_db)):
    ticker = ticker.upper()

    # --- DATABASE CHECK (The "Cache" Logic) ---
    last_record = db.query(models.SentimentResult).filter(
        models.SentimentResult.ticker == ticker
    ).order_by(models.SentimentResult.published_date.desc()).first()

    if last_record:
        time_elapsed = datetime.utcnow() - last_record.published_date
        
        # If record is less than 15 minutes old, pull from DB
        if time_elapsed < timedelta(minutes=15):
            return {
                "ticker": ticker,
                "status": "success",
                "source": "database", # Indicate data is from Database not live scraping
                "message": f"Showing existing data from database. Last updated {int(time_elapsed.total_seconds() // 60)}m ago.",
                "new_articles_saved": 0
            }

    # --- SCRAPING LOGIC (The "Live" Logic) ---
    news_items = get_financial_headlines(ticker)

    if isinstance(news_items, dict) and "error" in news_items:
        raise HTTPException(status_code=500, detail=news_items["error"])

    if not news_items:
        return {"message": f"No news found for {ticker}", "data": []}

    saved_count = 0
    results = []

    for item in news_items:
        if not isinstance(item, dict):
            continue

        existing = db.query(models.SentimentResult).filter(
            models.SentimentResult.link == item['link'],
            models.SentimentResult.ticker == ticker,
            models.SentimentResult.headline == item['headline']
        ).first()

        if not existing:
            score = nlp.analyze_sentiment(item.get('headline', ''))
            label = nlp.get_sentiment_label(score)

            new_record = models.SentimentResult(
                ticker=ticker,
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
    return {
        "ticker": ticker, 
        "source": "live",
        "new_articles_saved": saved_count, 
        "details": results
    }