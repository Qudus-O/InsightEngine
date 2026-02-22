import feedparser
import requests
import time
import random
from datetime import datetime

def get_financial_headlines(ticker: str):
    rss_url = f"https://finance.yahoo.com/rss/headline?s={ticker}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(rss_url, headers=headers, timeout=20)
        feed = feedparser.parse(response.content)

        results = []

        # Get top 10 headlines
        for entry in feed.entries[:10]: 
            
            # --- JITTER IMPLEMENTATION ---
            # Random sleep between 0.5 and 1.5 seconds per item
            # This makes the scraper's behavior look more human-like
            time.sleep(random.uniform(0.5, 1.5))

            # Clean the date format for PostgreSQL
            raw_date = getattr(entry, 'published', "")
            try:
                # Convert date and time to a standard format
                clean_date = datetime.strptime(raw_date, '%a, %d %b %Y %H:%M:%S %z').strftime('%Y-%m-%d %H:%M:%S')
            except:
                clean_date = raw_date

            results.append({
                "ticker": ticker.upper(),
                "headline": entry.title,
                "summary": getattr(entry, 'summary', "No summary available"),
                "date": clean_date,
                "source": "Yahoo Finance",
                "link": entry.link
            })
            
        return results

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    # Test the scraper
    print(f"Fetching news for NVDA with randomized jitter...")
    data = get_financial_headlines("NVDA")

    if isinstance(data, list):
        for idx, item in enumerate(data):
            print(f"{idx+1}. [{item['date']}] {item['headline']}")
    else:
        print(f"Error: {data.get('error')}")