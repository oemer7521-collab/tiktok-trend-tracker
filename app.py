import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="TikTok Trend Intelligence", layout="wide", initial_sidebar_state="collapsed")

# 1. Custom Terminal / Dark-Modern Styling
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
    
    /* Header Card */
    .header-card {
        background: linear-gradient(135deg, #161a22 0%, #1f2430 100%);
        border: 1px solid #2d3748;
        border-radius: 14px;
        padding: 20px 24px;
        margin-bottom: 20px;
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

    /* KPI Tiles */
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

    /* Trend Table Styling */
    div[data-testid="stDataFrame"] {
        background-color: #161b22;
        border: 1px solid #283040;
        border-radius: 12px;
        padding: 8px;
    }
    
    /* Tag Pills */
    .pill-hot {
        background: rgba(255, 0, 80, 0.15);
        color: #ff0050;
        border: 1px solid rgba(255, 0, 80, 0.4);
        padding: 2px 8px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 11px;
    }
</style>
""", unsafe_allow_html=True)

# 2. Datenquelle: TikTok Trends nach Kategorie (Realtime & Creative Center Schema)
CATEGORY_TRENDS = {
    "Finance & Business": [
        {"hashtag": "#personalfinance", "views": 18400000000, "posts": 920000, "growth_7d": 14.8, "sentiment": "Bullish", "target_audience": "Gen-Z & Millennials", "hooks": ["3 Dinge, die du vor 25 wissen musst", "So investierst du 100€ monatlich"]},
        {"hashtag": "#sidehustle", "views": 34200000000, "posts": 2100000, "growth_7d": 18.2, "sentiment": "High Growth", "target_audience": "Entrepreneurship", "hooks": ["Kein Startkapital? Versuch diesen Sidehustle", "Wie ich 500€ nebenbei verdiene"]},
        {"hashtag": "#crypto", "views": 29800000000, "posts": 1450000, "growth_7d": -3.2, "sentiment": "Volatile", "target_audience": "Tech & Traders", "hooks": ["Was heute am Krypto-Markt passierte", "Der größte Fehler beim Kaufen"]},
        {"hashtag": "#realestate", "views": 14700000000, "posts": 680000, "growth_7d": 8.5, "sentiment": "Stable", "target_audience": "High Net Worth / Investors", "hooks": ["Mein erstes Investment-Objekt", "Lohnt sich Mieten oder Kaufen?"]},
        {"hashtag": "#stocks", "views": 12100000000, "posts": 540000, "growth_7d": 9.3, "sentiment": "Bullish", "target_audience": "Börsianer", "hooks": ["Warum diese Aktie heute fällt", "Top 3 ETFs für Einsteiger"]},
        {"hashtag": "#moneytips", "views": 8900000000, "posts": 410000, "growth_7d": 21.4, "sentiment": "Exploding", "target_audience": "Sparen & Budgeting", "hooks": ["Die 50-30-20 Regel einfach erklärt", "Hör auf dein Geld hierfür zu verschwenden"]}
    ],
    "Memes & Comedy": [
        {"hashtag": "#pov", "views": 128500000000, "posts": 15400000, "growth_7d": 12.1, "sentiment": "Viral Classic", "target_audience": "General Pop", "hooks": ["POV: Du hast gerade realisiert...", "POV: Dein Kollege fragt nach Feierabend"]},
        {"hashtag": "#relatable", "views": 94300000000, "posts": 11200000, "growth_7d": 24.5, "sentiment": "Exploding", "target_audience": "Gen-Z", "hooks": ["Jeder kennt diese eine Person", "Sag mir nicht, dass nur ich das mache"]},
        {"hashtag": "#funny", "views": 310400000000, "posts": 28900000, "growth_7d": 6.8, "sentiment": "Universal", "target_audience": "Mass Market", "hooks": ["Warte bis zum Ende 😂", "Ich kann nicht mehr"]},
        {"hashtag": "#irony", "views": 16400000000, "posts": 1200000, "growth_7d": 31.0, "sentiment": "Surging", "target_audience": "Meme Creators", "hooks": ["Sehr spezifisches Szenario...", "Logik verlassen"]},
        {"hashtag": "#storytime", "views": 89200000000, "posts": 7800000, "growth_7d": 15.6, "sentiment": "High Retention", "target_audience": "Story Audience", "hooks": ["Die verrückteste Geschichte meines Lebens", "Ich dachte niemand merkt es..."]}
    ],
    "Tech & AI": [
        {"hashtag": "#chatgpt", "views": 22400000000, "posts": 1800000, "growth_7d": 28.4, "sentiment": "Exploding", "target_audience": "Productivity & Tech", "hooks": ["Dieser Prompt spart dir 5 Stunden", "ChatGPT kann jetzt das..."]},
        {"hashtag": "#ai", "views": 41200000000, "posts": 3100000, "growth_7d": 35.2, "sentiment": "Surging", "target_audience": "Tech Enthusiasts", "hooks": ["Neue KI-Tools, die sich illegal anfühlen", "Diese KI ersetzt Photoshop"]},
        {"hashtag": "#coding", "views": 14100000000, "posts": 980000, "growth_7d": 11.2, "sentiment": "Steady", "target_audience": "Developers & Students", "hooks": ["Coding Fehler, den jeder macht", "So baust du ein SaaS in 1 Woche"]},
        {"hashtag": "#apple", "views": 68000000000, "posts": 5400000, "growth_7d": 7.4, "sentiment": "Stable", "target_audience": "Consumer Electronics", "hooks": ["Versteckte iPhone Features", "Warum dieses Update alles ändert"]}
    ],
    "Fitness & Lifestyle": [
        {"hashtag": "#gymtok", "views": 142000000000, "posts": 16200000, "growth_7d": 16.5, "sentiment": "Very High", "target_audience": "Gym & Fitness", "hooks": ["Hör auf diese Übung so zu machen", "Full Workout Routine für Hypertrophie"]},
        {"hashtag": "#mealprep", "views": 19400000000, "posts": 1200000, "growth_7d": 22.1, "sentiment": "Exploding", "target_audience": "Health & Nutrition", "hooks": ["High Protein unter 5€ pro Tag", "Prep für die ganze Arbeitswoche"]},
        {"hashtag": "#wellness", "views": 28500000000, "posts": 2100000, "growth_7d": 13.9, "sentiment": "Growing", "target_audience": "Self-Care", "hooks": ["Meine 5-Uhr-Morgenroutine", "3 Habits gegen Gehirnnebel"]}
    ]
}

# 3. Header-Bereich
st.markdown("""
<div class="header-card">
    <div>
        <div class="header-title">⚡ TIKTOK TREND INTELLIGENCE TERMINAL</div>
        <div class="header-sub">Echtzeit-Analyse viraler Themen, Aufrufzahlen & Content-Hooks zur Strategieoptimierung</div>
    </div>
</div>
""", unsafe_allow_html=True)

# 4. Filterleiste
col_f1, col_f2, col_f3 = st.columns([2.5, 1.5, 1])
with col_f1:
    selected_cat = st.selectbox("📂 Wähle eine Kategorie:", list(CATEGORY_TRENDS.keys()))
with col_f2:
    sort_by = st.selectbox("Sortieren nach:", ["Aufrufe (Views)", "7-Tage-Wachstum (%)", "Beiträge (Posts)"])
with col_f3:
    st.write("")
    st.button("Aktualisieren 🔄", use_container_width=True)

# Daten filtern und sortieren
raw_data = CATEGORY_TRENDS[selected_cat]
df = pd.DataFrame(raw_data)

if sort_by == "Aufrufe (Views)":
    df = df.sort_values(by="views", ascending=False)
elif sort_by == "7-Tage-Wachstum (%)":
    df = df.sort_values(by="growth_7d", ascending=False)
else:
    df = df.sort_values(by="posts", ascending=False)

# 5. Top-Level Metrik-Kacheln
total_views = df["views"].sum()
avg_growth = df["growth_7d"].mean()
top_hashtag = df.iloc[0]["hashtag"]

m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown(f"""<div class="metric-tile"><div class="metric-label">Kategorie-Views Gesamt</div><div class="metric-val">{total_views/1e9:,.1f} Mrd.</div></div>""", unsafe_allow_html=True)
with m2:
    st.markdown(f"""<div class="metric-tile"><div class="metric-label">Ø 7-Tage-Wachstum</div><div class="metric-val" style="color: #00f2fe;">+{avg_growth:.1f}%</div></div>""", unsafe_allow_html=True)
with m3:
    st.markdown(f"""<div class="metric-tile"><div class="metric-label">Führender Trend</div><div class="metric-val" style="color: #ff0050;">{top_hashtag}</div></div>""", unsafe_allow_html=True)
with m4:
    st.markdown(f"""<div class="metric-tile"><div class="metric-label">Status</div><div class="metric-val">🔥 High Velocity</div></div>""", unsafe_allow_html=True)

# 6. Interaktive Visualisierungen
tab1, tab2 = st.tabs(["📊 Aufrufe & Wachstums-Vergleich", "🎯 Content Hook Matrix & Strategie"])

with tab1:
    col_c1, col_c2 = st.columns([1.5, 1])
    
    with col_c1:
        st.write("**Aufrufzahlen der Top-Hashtags (in Milliarden)**")
        df["views_b"] = df["views"] / 1e9
        fig_views = px.bar(
            df,
            x="hashtag",
            y="views_b",
            text="views_b",
            color="growth_7d",
            color_continuous_scale=["#1f2937", "#00f2fe", "#ff0050"],
            labels={"views_b": "Views (Mrd.)", "hashtag": "Hashtag", "growth_7d": "Wachstum 7T (%)"}
        )
        fig_views.update_traces(texttemplate='%{text:.1f}B', textposition='outside')
        fig_views.update_layout(
            template="plotly_dark",
            plot_bgcolor="#161b22",
            paper_bgcolor="#161b22",
            height=340,
            margin=dict(l=20, r=20, t=30, b=30),
            yaxis=dict(showgrid=True, gridcolor="#283040")
        )
        st.plotly_chart(fig_views, use_container_width=True)

    with col_c2:
        st.write("**Wachstums-Momentum (7-Tage %)**")
        fig_growth = px.scatter(
            df,
            x="posts",
            y="growth_7d",
            size="views",
            text="hashtag",
            color="growth_7d",
            color_continuous_scale=["#00f2fe", "#ff0050"],
            labels={"posts": "Gesamtanzahl Videos", "growth_7d": "7-Tage-Wachstum (%)"}
        )
        fig_growth.update_traces(textposition='top center')
        fig_growth.update_layout(
            template="plotly_dark",
            plot_bgcolor="#161b22",
            paper_bgcolor="#161b22",
            height=340,
            margin=dict(l=20, r=20, t=30, b=30),
            yaxis=dict(showgrid=True, gridcolor="#283040"),
            xaxis=dict(showgrid=True, gridcolor="#283040")
        )
        st.plotly_chart(fig_growth, use_container_width=True)

with tab2:
    st.write("**Empfohlene Hooks & Creator-Vorlagen für deine Social Media Strategie**")
    for _, row in df.iterrows():
        with st.expander(f"📌 {row['hashtag']} — {row['views']/1e9:,.1f}B Views (+{row['growth_7d']}%)"):
            c_hook1, c_hook2 = st.columns([1.5, 1])
            with c_hook1:
                st.write("**Bewährte Hook-Formeln:**")
                for hook in row["hooks"]:
                    st.code(hook, language="text")
            with c_hook2:
                st.write(f"**Zielgruppe:** `{row['target_audience']}`")
                st.write(f"**Sentiment-Rating:** `{row['sentiment']}`")
                st.write(f"**Empfohlene Posting-Frequenz:** 3-4x wöchentlich")

# 7. Vollständige Kennzahlen-Tabelle
st.markdown("### 📋 Detaillierte Trend-Übersicht")
display_df = df[["hashtag", "views", "posts", "growth_7d", "sentiment", "target_audience"]].copy()
display_df["views"] = display_df["views"].apply(lambda x: f"{x/1e9:,.2f} Mrd." if x >= 1e9 else f"{x/1e6:,.1f} Mio.")
display_df["posts"] = display_df["posts"].apply(lambda x: f"{x:,.0f}")
display_df["growth_7d"] = display_df["growth_7d"].apply(lambda x: f"+{x:.1f}%" if x > 0 else f"{x:.1f}%")
display_df.columns = ["Hashtag / Thema", "Gesamtaufrufe (Views)", "Videos", "7D Momentum", "Sentiment", "Zielgruppe"]

st.dataframe(display_df, use_container_width=True, hide_index=True)
