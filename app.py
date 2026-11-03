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
            {"hashtag": "#foodtokdeutschland", "views": 11300000000, "posts": 1400000, "growth_7d": 21.0, "sentiment": "Viral Food", "target_audience": "Foodies & Kochen", "hooks": ["Der beste Döner in deiner Stadt", "Schnelles 15-Minuten Feierabend-Rezept", "Airfryer Hacks, die dein Leben verändern"]}
        ]
    },
    "🌍 Global (Weltweit)": {
        "Finance & Business": [
            {"hashtag": "#personalfinance", "views": 18400000000, "posts": 920000, "growth_7d": 14.8, "sentiment": "Bullish", "target_audience": "Gen-Z & Millennials", "hooks": ["3 things you must know before 25", "How to invest $100 monthly"]},
            {"hashtag": "#sidehustle", "views": 34200000000, "posts": 2100000, "growth_7d": 18.2, "sentiment": "High Growth", "target_audience": "Entrepreneurs", "hooks": ["Zero capital? Try this side hustle", "How I make $500 on weekends"]},
            {"hashtag": "#crypto", "views": 29800000000, "posts": 1450000, "growth_7d": -3.2, "sentiment": "Volatile", "target_audience": "Traders", "hooks": ["What just happened in crypto today", "The biggest mistake buying Bitcoin"]}
        ],
        "Memes & Comedy": [
            {"hashtag": "#pov", "views": 128500000000, "posts": 15400000, "growth_7d": 12.1, "sentiment": "Viral Classic", "target_audience": "General Pop", "hooks": ["POV: You just realized...", "POV: Your coworker asks for help at 5 PM"]},
            {"hashtag": "#relatable", "views": 94300000000, "posts": 11200000, "growth_7d": 24.5, "sentiment": "Exploding", "target_audience": "Gen-Z", "hooks": ["Everyone knows this one person", "Don't tell me I'm the only one"]}
        ],
        "Sport & Lifestyle": [
            {"hashtag": "#gymtok", "views": 142000000000, "posts": 16200000, "growth_7d": 16.5, "sentiment": "Very High", "target_audience": "Fitness & Gym", "hooks": ["Stop doing this exercise like this", "Full hypertrophy routine"]},
            {"hashtag": "#mealprep", "views": 19400000000, "posts": 1200000, "growth_7d": 22.1, "sentiment": "Exploding", "target_audience": "Nutrition", "hooks": ["High protein under $5 a day", "Prep for the entire week"]}
        ]
    }
}

# 3. Header-Banner
st.markdown("""
<div class="header-card">
    <div>
        <div class="header-title">⚡ TIKTOK TREND INTELLIGENCE</div>
        <div class="header-sub">Echtzeit-Analyse regionaler Trends, Aufrufzahlen & viraler Video-Hooks</div>
    </div>
</div>
""", unsafe_allow_html=True)

# 4. Filterleiste mit Regions-Umschalter
f_col1, f_col2, f_col3, f_col4 = st.columns([1.5, 2, 1.5, 1])
with f_col1:
    region = st.selectbox("📍 Region / Markt:", list(TREND_DATABASE.keys()))
with f_col2:
    available_categories = list(TREND_DATABASE[region].keys())
    selected_cat = st.selectbox("📂 Kategorie:", available_categories)
with f_col3:
    sort_by = st.selectbox("Sortieren nach:", ["Aufrufe (Views)", "7-Tage-Wachstum (%)", "Beiträge (Posts)"])
with f_col4:
    st.write("")
    st.button("Aktualisieren 🔄", use_container_width=True)

# Daten filtern und sortieren
raw_data = TREND_DATABASE[region][selected_cat]
df = pd.DataFrame(raw_data)

if sort_by == "Aufrufe (Views)":
    df = df.sort_values(by="views", ascending=False)
elif sort_by == "7-Tage-Wachstum (%)":
    df = df.sort_values(by="growth_7d", ascending=False)
else:
    df = df.sort_values(by="posts", ascending=False)

# 5. Top-Level Kennzahlen
total_views = df["views"].sum()
avg_growth = df["growth_7d"].mean()
top_hashtag = df.iloc[0]["hashtag"]

m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown(f"""<div class="metric-tile"><div class="metric-label">Kategorie-Views ({region.split()[0]})</div><div class="metric-val">{total_views/1e9:,.2f} Mrd.</div></div>""", unsafe_allow_html=True)
with m2:
    st.markdown(f"""<div class="metric-tile"><div class="metric-label">Ø 7-Tage-Wachstum</div><div class="metric-val" style="color: #00f2fe;">+{avg_growth:.1f}%</div></div>""", unsafe_allow_html=True)
with m3:
    st.markdown(f"""<div class="metric-tile"><div class="metric-label">Top Trend</div><div class="metric-val" style="color: #ff0050;">{top_hashtag}</div></div>""", unsafe_allow_html=True)
with m4:
    st.markdown(f"""<div class="metric-tile"><div class="metric-label">Region Status</div><div class="metric-val">🔥 Hohe Relevanz</div></div>""", unsafe_allow_html=True)

# 6. Interaktive Diagramme
tab1, tab2 = st.tabs(["📊 Aufrufe & Momentum", "🎯 Hook-Matrix & Content-Strategie"])

with tab1:
    col_c1, col_c2 = st.columns([1.5, 1])
    
    with col_c1:
        st.write(f"**Top Hashtags nach Aufrufzahlen ({region})**")
        df["views_b"] = df["views"] / 1e9
        fig_views = px.bar(
            df,
            x="hashtag",
            y="views_b",
            text="views_b",
            color="growth_7d",
            color_continuous_scale=["#1f2937", "#00f2fe", "#ff0050"],
            labels={"views_b": "Views (Mrd.)", "hashtag": "Hashtag", "growth_7d": "Wachstum (%)"}
        )
        fig_views.update_traces(texttemplate='%{text:.1f} Mrd.', textposition='outside')
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
        st.write("**Wachstumsrate vs. Beitragsdichte**")
        fig_growth = px.scatter(
            df,
            x="posts",
            y="growth_7d",
            size="views",
            text="hashtag",
            color="growth_7d",
            color_continuous_scale=["#00f2fe", "#ff0050"],
            labels={"posts": "Anzahl Videos", "growth_7d": "7-Tage-Wachstum (%)"}
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
    st.write(f"**Empfohlene Video-Hooks für {region} ({selected_cat})**")
    for _, row in df.iterrows():
        with st.expander(f"📌 {row['hashtag']} — {row['views']/1e9:,.2f} Mrd. Views (+{row['growth_7d']}%)"):
            c_hook1, c_hook2 = st.columns([1.5, 1])
            with c_hook1:
                st.write("**Top virale Hook-Formeln:**")
                for hook in row["hooks"]:
                    st.code(hook, language="text")
            with c_hook2:
                st.write(f"**Zielgruppe:** `{row['target_audience']}`")
                st.write(f"**Dynamik:** `{row['sentiment']}`")
                st.write(f"**Strategie:** 3-5 relevante Hashtags kombinieren")

# 7. Tabelle
st.markdown(f"### 📋 Alle Kennzahlen für {region}")
display_df = df[["hashtag", "views", "posts", "growth_7d", "sentiment", "target_audience"]].copy()
display_df["views"] = display_df["views"].apply(lambda x: f"{x/1e9:,.2f} Mrd." if x >= 1e9 else f"{x/1e6:,.1f} Mio.")
display_df["posts"] = display_df["posts"].apply(lambda x: f"{x:,.0f}")
display_df["growth_7d"] = display_df["growth_7d"].apply(lambda x: f"+{x:.1f}%" if x > 0 else f"{x:.1f}%")
display_df.columns = ["Hashtag", "Aufrufe (Views)", "Videos", "7D Momentum", "Status", "Zielgruppe"]

st.dataframe(display_df, use_container_width=True, hide_index=True)
