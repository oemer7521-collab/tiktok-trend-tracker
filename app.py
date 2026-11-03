import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="TikTok Trend Intelligence DACH & Global", layout="wide", initial_sidebar_state="collapsed")

# 1. Dark Modern Styling
st.markdown("""
<style>
    .stApp {
        background-color: #0d0f12;
        color: #f1f5f9;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 3rem !important;
        max-width: 95% !important;
    }
    
    .header-card {
        background: linear-gradient(135deg, #161a22 0%, #1f2430 100%);
        border: 1px solid #2d3748;
        border-radius: 14px;
        padding: 20px 24px;
        margin-bottom: 18px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .header-title {
        font-size: 24px;
        font-weight: 800;
        letter-spacing: -0.5px;
        background: linear-gradient(90deg, #ff0050 0%, #00f2fe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .header-sub {
        font-size: 13px;
        color: #94a3b8;
        margin-top: 4px;
    }

    .metric-tile {
        background: #161b22;
        border: 1px solid #283040;
        border-radius: 12px;
        padding: 14px 18px;
        margin-bottom: 14px;
    }
    .metric-label {
        font-size: 12px;
        text-transform: uppercase;
        color: #94a3b8;
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    .metric-val {
        font-size: 22px;
        font-weight: 700;
        color: #f8fafc;
        margin-top: 4px;
    }

    div[data-testid="stDataFrame"] {
        background-color: #161b22;
        border: 1px solid #283040;
        border-radius: 12px;
        padding: 8px;
    }

    .country-pill {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: 700;
        background: rgba(0, 242, 254, 0.15);
        color: #00f2fe;
        border: 1px solid rgba(0, 242, 254, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# 2. Datensatz: Aufgeteilt nach Region (Global vs. Deutschland)
TREND_DATABASE = {
    "🇩🇪 Deutschland (DACH)": {
        "Finance & Business": [
            {"hashtag": "#finanztok", "views": 3200000000, "posts": 340000, "growth_7d": 19.4, "sentiment": "Exploding", "target_audience": "Deutsche Gen-Z & Berufseinsteiger", "hooks": ["3 Steuer-Tricks, die dein Finanzamt hasst", "So sparst du 300€ jeden Monat in Deutschland", "ETF Sparplan für Anfänger erklärt"]},
            {"hashtag": "#aktientipps", "views": 1850000000, "posts": 180000, "growth_7d": 14.2, "sentiment": "Bullish", "target_audience": "Privatanleger / DAX-Interessierte", "hooks": ["Warum Trade Republic heute crasht", "Die beste Dividendenaktie Deutschlands", "Mein Aktien-Depot Update für diesen Monat"]},
            {"hashtag": "#steuertipps", "views": 2400000000, "posts": 290000, "growth_7d": 23.8, "sentiment": "Surging", "target_audience": "Angestellte & Selbstständige", "hooks": ["Das kannst du sofort von der Steuer absetzen", "Vorsicht vor dieser Steuerfalle 2026", "Werbungskostenpauschale richtig nutzen"]},
            {"hashtag": "#studium", "views": 5900000000, "posts": 810000, "growth_7d": 11.5, "sentiment": "High Engagement", "target_audience": "Studenten & Abiturienten", "hooks": ["Bafög-Geheimnis, das niemand erzählt", "So lernst du für Klausuren in 3 Tagen", "Studenten-Rabatte, die sich lohnen"]},
            {"hashtag": "#immobilien", "views": 2100000000, "posts": 160000, "growth_7d": 8.7, "sentiment": "Stable", "target_audience": "Kapitalanleger", "hooks": ["Wohnung kaufen in Berlin / München: Lohnt es sich?", "Wie ich mit 23 meine erste Immobilie kaufte"]}
        ],
        "Memes & Comedy": [
            {"hashtag": "#deutschmeme", "views": 18400000000, "posts": 2400000, "growth_7d": 26.5, "sentiment": "Viral", "target_audience": "Deutsche Community", "hooks": ["Deutsche, wenn der Zug 2 Minuten zu spät kommt", "Typisch deutsche Mütter sonntags", "POV: Du bist auf einer deutschen Behörde"]},
            {"hashtag": "#comedydeutschland", "views": 14200000000, "posts": 1900000, "growth_7d": 18.2, "sentiment": "High Velocity", "target_audience": "Breites Publikum", "hooks": ["Warte bis du den Schluss siehst...", "Jeder Deutsche kennt genau diesen Moment", "Wenn der Chef am Freitag um 16 Uhr anruft"]},
            {"hashtag": "#alman", "views": 9800000000, "posts": 1300000, "growth_7d": 12.8, "sentiment": "Evergreen", "target_audience": "Gen-Z & Millennials", "hooks": ["Endlevel Alman Verhalten", "Wenn du die Rechnung im Restaurant durch 4 teilst", "Alman-Eltern im Sommerurlaub"]},
            {"hashtag": "#lustigevideos", "views": 22100000000, "posts": 3100000, "growth_7d": 8.4, "sentiment": "Universal", "target_audience": "Masse", "hooks": ["Ich kann das alles nicht mehr 😂", "Wer kennt es auch? Markiert eure Freunde"]}
        ],
        "Sport & Lifestyle": [
            {"hashtag": "#bundesliga", "views": 24800000000, "posts": 3200000, "growth_7d": 32.1, "sentiment": "Trending", "target_audience": "Fußballfans", "hooks": ["Die größte Fehlentscheidung des Spieltags", "Warum Bayern / BVB dieses Spiel verloren hat", "Reaktion auf das Tor des Monats"]},
            {"hashtag": "#gymdeutschland", "views": 4900000000, "posts": 580000, "growth_7d": 17.6, "sentiment": "High Growth", "target_audience": "Fitness & Bodybuilding", "hooks": ["Die beste Gymshark / ESN Alternative", "Warum du bei Kniebeugen keine Gains machst", "Mein Full Day of Eating für Muskelaufbau"]},
            {"hashtag": "#foodtokdeutschland", "views": 11300000000, "posts": 1400000, "growth_7d":
