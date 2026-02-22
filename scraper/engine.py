import feedparser
import requests
from datetime import datetime




def get_financial_headlines(ticker: str):

    rss_url = f"https://finance.yahoo.com/rss/headline?s={ticker}"

    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(rss_url, headers=headers, timeout=20)
        feed = feedparser.parse(response.content)

        results = []

        for entry in feed.entries[:10]: # Get 10 headlines for better data

            # Clean the date format for PostgreSQL later

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

    data = get_financial_headlines("NVDA")

    for idx, item in enumerate(data):
        print(f"{idx+1}. [{item['date']}] {item['headline']}")




