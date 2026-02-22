from sqlalchemy import Column, Integer, String, Float, DateTime, Text, UniqueConstraint
from .database import Base
import datetime

class SentimentResult(Base):
    __tablename__ = "sentiment_results"         

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String(10), nullable=False, index=True)
    headline = Column(Text, nullable=False)
    summary = Column(Text)
    sentiment_score = Column(Float, nullable=False)
    sentiment_label = Column(String(20), nullable=False)
    published_date = Column(DateTime)
    source = Column(String(50))
    link = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    __table_args__ = (
        UniqueConstraint('ticker', 'link', 'headline', name='ticker_link_headline_unique'),
    )