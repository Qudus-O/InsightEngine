import streamlit as st
import pandas as pd
import plotly.express as px
import httpx
import os
import asyncio

from sqlalchemy import create_engine
from dotenv import load_dotenv
from datetime import datetime

# Configuration and Styling
st.set_page_config(page_title="InsightEngine", layout="wide", page_icon="📈")
load_dotenv()

# Database and API Connection
DATABASE_URL = os.getenv("DATABASE_URL")
API_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000") # check backend url or use default localhost
engine = create_engine(DATABASE_URL)

# Sidebar - Controls
st.sidebar.header("🔍 Controls")
ticker = st.sidebar.text_input("Stock Ticker (e.g., TSLA, NVDA, AAPL)").upper()
analyze_btn = st.sidebar.button("Run New Analysis")

# Functions and Data Handling
def fetch_data(symbol):
    query = f"SELECT * FROM sentiment_results WHERE ticker = '{symbol}' ORDER BY published_date DESC"
    return pd.read_sql(query, engine)

async def trigger_backend(symbol):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{API_URL}/analyze/{symbol}", timeout=30)
            return response.json()
        except Exception as e:
            return {"error": str(e)}

# --- MAIN UI FLOW ---

if not ticker:
    # WELCOME DASHBOARD
    st.title("🚀 InsightEngine")
    st.subheader("Your AI-Powered Financial Sentiment Command Center")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        ### Intelligence Overview
        InsightEngine uses **VADER NLP** and **FastAPI** to scrape and analyze 
        real-time financial news. 
        
        **How to use:**
        1. Enter a ticker symbol in the sidebar.
        2. Click **Run New Analysis** to fetch live data.
        3. View historical trends and market mood instantly.
        """)
    
    with col2:
        try:
            # Dynamic stats from your actual database
            distinct_tickers = pd.read_sql("SELECT COUNT(DISTINCT ticker) FROM sentiment_results", engine).iloc[0,0]
            total_records = pd.read_sql("SELECT COUNT(*) FROM sentiment_results", engine).iloc[0,0]
            
            st.metric("Companies Tracked", distinct_tickers)
            st.metric("Headlines Analyzed", total_records)
            st.success("✅ Database Connection: Active")
        except:
            st.info("👋 Welcome! Search for a ticker to begin populating your local intelligence database.")

    st.divider()
    # High-quality financial image for professional look
    st.image("https://images.unsplash.com/photo-1611974717482-982da61e65b2?auto=format&fit=crop&q=80&w=1000", 
             caption="Real-time Sentiment Analysis Pipeline")

else:
    # DISPLAY TICKER INTELLIGENCE
    st.title(f"📊 Market Intelligence: {ticker}")
    
    if analyze_btn:
        with st.spinner(f"Requesting data for {ticker}..."):
            result = asyncio.run(trigger_backend(ticker))
            if "error" in result:
                st.error(f"Backend Error: {result['error']}")
            else:
                # Show the recommendation-based source badge (Database vs Live)
                source_type = result.get('source', 'live').upper()
                if source_type == "DATABASE":
                    st.toast(f"Retrieved from Database (Freshness Guaranteed)", icon="🗄️")
                else:
                    st.toast(f"Live Scrape Complete!", icon="🌐")
                
                st.success(f"Done! {result.get('new_articles_saved', 0)} new articles added to intelligence bank.")

    # Fetch and Display Data
    df = fetch_data(ticker)

    if not df.empty:
        # --- METRICS SECTION ---
        avg_score = df['sentiment_score'].mean()
        mood = "BULLISH" if avg_score > 0.05 else "BEARISH" if avg_score < -0.05 else "NEUTRAL"
        
        m_col1, m_col2, m_col3 = st.columns(3)
        m_col1.metric("Headlines", len(df))
        m_col2.metric("Avg Sentiment", round(avg_score, 3))
        m_col3.metric("Current Mood", mood)

        # --- SENTIMENT TREND CHART ---
        st.subheader("Sentiment Trend Analysis")
        df['published_date'] = pd.to_datetime(df['published_date'])
        fig = px.line(df, x='published_date', y='sentiment_score', 
                      title=f"Sentiment Volatility: {ticker}",
                      markers=True, template="plotly_dark",
                      color_discrete_sequence=['#00CC96']) # Professional green line
        st.plotly_chart(fig, use_container_width=True)

        # --- DATA TABLE SECTION ---
        with st.expander("View Raw Intelligence Data"):
            st.dataframe(df[['published_date', 'headline', 'sentiment_label', 'sentiment_score', 'link']], 
                         use_container_width=True)
    else:
        st.warning(f"No data found for {ticker} in the database. Please click 'Run New Analysis' to fetch the latest news.")


