import streamlit as st
import pandas as pd
import openai
import requests
import plotly.graph_objects as go

# --- SYSTEM ARCHITECTURE ---
st.set_page_config(page_title="TITAN OMNI-OS", layout="wide", page_icon="🌌")

# Ultra-Dark HUD Styling
st.markdown("""
    <style>
    .main { background-color: #050505; color: #00ff41; font-family: 'Courier New', Courier, monospace; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { background-color: #111; border-radius: 5px; color: #00ff41; padding: 10px 20px; }
    .stMetric { background-color: #0a0a0a; border: 1px solid #00ff41; padding: 15px; border-radius: 5px; }
    </style>
    """, unsafe_allow_globals=True)

# --- THE VAULT: SIDEBAR ---
with st.sidebar:
    st.title("🛡️ OMNI-CORE ACCESS")
    api_key = st.text_input("Master Neural Key (OpenAI)", type="password")
    alpha_key = st.text_input("Market Data Key (Alpha Vantage)", type="password")
    
    st.divider()
    st.header("📡 Uplink Settings")
    st.info("System optimized for North Merritt Island, FL")
    if api_key and alpha_key:
        st.success("All Systems GO")

# --- DATA & AI ENGINES ---
def get_market_data(symbol):
    if not alpha_key: return None
    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={alpha_key}'
    r = requests.get(url)
    return r.json().get('Global Quote', {})

def titan_ai(prompt, mode):
    if not api_key: return "API Key Missing."
    client = openai.OpenAI(api_key=api_key)
    personas = {
        "wealth": "You are a master financial architect. Focus on ROI and wealth building.",
        "engineer": "You are a master of physics and automotive engineering for racing.",
        "scholar": "You are a universal scholar. You teach any language or science perfectly."
    }
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": personas[mode]}, {"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# --- MAIN INTERFACE ---
tabs = st.tabs(["💎 WEALTH", "⚙️ ENGINEERING", "🌍 SCHOLAR", "👁️ VISION"])

# --- TAB 1: WEALTH (NO YFINANCE) ---
with tabs[0]:
    st.header("💰 Financial Intelligence")
    col1, col2 = st.columns([1, 2])
    with col1:
        ticker = st.text_input("Asset Ticker", "TSLA").upper()
        if st.button("Deep Quant Scan"):
            data = get_market_data(ticker)
            if data:
                price = data.get('05. price', 'N/A')
                change = data.get('10. change percent', 'N/A')
                st.metric(f"{ticker} Current", f"${price}", change)
                
                analysis = titan_ai(f"Analyze {ticker} for a long-term wealth strategy.", "wealth")
                st.write(analysis)
            else:
                st.error("Enter Alpha Vantage Key in Sidebar.")

# --- TAB 2: ENGINEERING ---
with tabs[1]:
    st.header("🛠️ Engineering & Applied Physics")
    eng_q = st.text_area("Input technical build problems (Mustang/Massimo/Aero)")
    if st.button("Consult Engineer"):
        st.markdown(titan_ai(eng_q, "engineer"))
    
    # Quick Performance Calculator
    st.divider()
    r1, r2 = st.columns(2)
    weight = r1.number_input("Weight (lbs)", value=3500)
    hp = r2.number_input("HP", value=412)
    st.metric("Est. 1/4 Mile Time", f"{5.825 * ((weight/hp)**(1/3)):.2f}s")

# --- TAB 3: SCHOLAR ---
with tabs[2]:
    st.header("📚 Universal Library")
    subject = st.selectbox("Subject", ["Mathematics", "Physics", "Languages", "JROTC"])
    q = st.text_area(f"Explain {subject} concept...")
    if st.button("Acquire Knowledge"):
        st.write(titan_ai(q, "scholar"))

# --- TAB 4: VISION ---
with tabs[3]:
    st.header("👁️ Neural Vision")
    cam = st.camera_input("Scanner Active")
    if cam:
        st.info("Visual Data Stream Captured.")
