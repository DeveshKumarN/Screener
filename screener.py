import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

def calculate_rsi(prices_series, period=14):
    """Custom RSI calculation."""
    deltas = np.diff(prices_series)
    seed = deltas[:period]
    up = seed[seed >= 0].sum() / period
    down = -seed[seed < 0].sum() / period
    
    rs = up / down if down != 0 else 0
    rsi = np.zeros_like(prices_series)
    rsi[:period] = 100. - 100. / (1. + rs)

    for i in range(period, len(prices_series)):
        delta = deltas[i - 1]
        upval = delta if delta > 0 else 0.
        downval = -delta if delta < 0 else 0.

        up = (up * (period - 1) + upval) / period
        down = (down * (period - 1) + downval) / period
        rs = up / down if down != 0 else 0
        rsi[i] = 100. - 100. / (1. + rs)
        
    return rsi[-1]

def calculate_ema(prices, days):
    """Custom Exponential Moving Average using manual array weighting."""
    ema = np.zeros_like(prices)
    multiplier = 2 / (days + 1)
    ema[0] = prices[0]
    
    for i in range(1, len(prices)):
        ema[i] = (prices[i] - ema[i-1]) * multiplier + ema[i-1]
    return ema

def calculate_macd(prices):
    """Calculates MACD Line and Histogram (12-day EMA vs 26-day EMA)."""
    if len(prices) < 26:
        return 0, 0
    
    ema_12 = calculate_ema(prices, 12)
    ema_26 = calculate_ema(prices, 26)
    
    macd_line = ema_12 - ema_26
    signal_line = calculate_ema(macd_line, 9)
    macd_histogram = macd_line[-1] - signal_line[-1]
    
    return macd_line[-1], macd_histogram

@st.cache_data(ttl=300) 
def fetch_market_data(tickers):
    """Fetches live data and computes all signals."""
    results = []
    data = yf.download(tickers, period="1y", interval="1d", group_by="ticker", progress=False)
    
    for ticker in tickers:
        try:
            df = data[ticker] if len(tickers) > 1 else data
            if df.empty: continue
            
            closes = df['Close'].dropna().values
            if len(closes) < 100: continue
            
            current_price = closes[-1]
            prev_price = closes[-2]
            
            # Indicators
            rsi = calculate_rsi(closes)
            macd_val, macd_hist = calculate_macd(closes)
            mda_100 = np.mean(closes[-100:]) 

            momentum = "Bullish 📈" if current_price > prev_price else "Bearish 📉"

            if rsi >= 80:
                rsi_status = "Overbought 🔥"
            elif rsi <= 40:
                rsi_status = "Oversold 🧊"
            else:
                rsi_status = "Neutral ⚖️"

            if macd_hist > 0:
                macd_status = "Positive (Buy) 🟢"
            else:
                macd_status = "Negative (Sell) 🔴"
                
            results.append({
                "Ticker": ticker,
                "Price": round(current_price, 2),
                "100-Day MDA": round(mda_100, 2),
                "MACD": round(macd_val, 2),
                "MACD Signal": macd_status,
                "RSI": round(rsi, 2),
                "Momentum": momentum,
                "Status": rsi_status
            })
        except Exception:
            pass 
            
    return pd.DataFrame(results)

def show_screener():
    st.markdown("""<style>[data-testid="collapsedControl"] {display: block;}</style>""", unsafe_allow_html=True)
    
    st.sidebar.success(f"Active User:\n**{st.session_state.user_email}**")
    if st.sidebar.button("Log Out"):
        st.session_state.logged_in = False
        st.session_state.user_email = ""
        st.session_state.current_page = 'login'
        st.rerun()
        
    st.title("📊 Live Market Screener")
    st.write("Tracking top US equities with algorithmic RSI, MACD, and 100-Day MDA analysis.")
    
    top_tickers = [
        "AAPL", "MSFT", "NVDA", "AMZN", "META", "GOOGL", "BRK-B", "LLY", "AVGO", "TSLA",
        "JPM", "V", "WMT", "UNH", "MA", "PG", "JNJ", "HD", "MRK", "ORCL"
    ]
    
    with st.spinner("Fetching live market data and computing algorithms..."):
        df = fetch_market_data(top_tickers)
        
    if not df.empty:
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        st.subheader("🚨 Active Alerts")
        for _, row in df.iterrows():
            if row['Status'] == "Overbought 🔥":
                st.error(f"**{row['Ticker']}** is Overbought (RSI: {row['RSI']}) - Potential Reversal!")
                st.toast(f"{row['Ticker']} Overbought!", icon="🔥")
            elif row['Status'] == "Oversold 🧊":
                st.success(f"**{row['Ticker']}** is Oversold (RSI: {row['RSI']}) - Potential Bounce!")
                st.toast(f"{row['Ticker']} Oversold!", icon="🧊")
            
            if row['Status'] == "Oversold 🧊" and "Buy" in row['MACD Signal']:
                st.info(f"**{row['Ticker']}** shows a strong double convergence: Oversold RSI + Positive MACD.")