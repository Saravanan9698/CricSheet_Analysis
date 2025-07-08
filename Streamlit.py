import streamlit as st
import pandas as pd
import base64
import plotly.express as px
from datetime import datetime

# Paths
DATA_PATHS = {
    "IPL": r"D:\Projects\Mini_Projects\CricSheet_Analysis\CSV_Datasets\ipl_json_combined_cleaned.csv",
    "ODI": r"D:\Projects\Mini_Projects\CricSheet_Analysis\CSV_Datasets\odis_json_combined_cleaned.csv",
    "T20I": r"D:\Projects\Mini_Projects\CricSheet_Analysis\CSV_Datasets\t20s_json_combined_cleaned.csv",
    "TEST": r"D:\Projects\Mini_Projects\CricSheet_Analysis\CSV_Datasets\tests_json_combined_cleaned.csv"
}
IMAGE_PATH = "Image/Cricpic.jpg"

# Load background image and convert to base64
def img_to_base64(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        return None

img_base64 = img_to_base64(IMAGE_PATH)

# Streamlit app background styling
if img_base64:
    st.markdown(f"""
        <style>
        .stApp {{
            background-image: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), 
                              url("data:image/jpeg;base64,{img_base64}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        .hero {{
            text-align: center;
            color: white;
            padding-top: 250px;
            padding-bottom: 60px;
        }}
        .hero h1 {{ font-size: 60px; margin-bottom: 10px; }}
        .hero h3 {{ font-size: 26px; font-weight: 300; }}
        </style>
        <div class="hero">
            <h1>Cricsheet Match Analysis</h1>
            <h3>Explore IPL, ODI, T20I, and TEST Match Statistics</h3>
        </div>
    """, unsafe_allow_html=True)

# Sidebar format selector
st.sidebar.title("🔍 Explore Formats")
selected_format = st.sidebar.radio("Select Match Type", list(DATA_PATHS.keys()))

# Load dataset
@st.cache_data
def load_data(file_path):
    df = pd.read_csv(file_path)
    if "Year" not in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors='coerce')
        df["Year"] = df["Date"].dt.year
    return df

df = load_data(DATA_PATHS[selected_format])

# Metrics Section
st.markdown("## 🧾 Quick Overview")
col1, col2, col3, col4 = st.columns(4)
col1.metric("🏏 Total Matches", df["Match_Number"].nunique())
col2.metric("👥 Teams", df["Teams_Participated"].nunique())
col3.metric("📍 Venues", df["Venue"].nunique())
col4.metric("📆 Seasons", df["Season"].nunique())

# Visualizations
st.markdown("---")
st.markdown("## 📊 Key Insights")

col5, col6 = st.columns(2)

with col5:
    matches_per_year = df["Year"].value_counts().sort_index().reset_index()
    matches_per_year.columns = ["Year", "Matches"]
    fig1 = px.bar(matches_per_year, x="Year", y="Matches", title="Matches Per Year", color="Matches")
    st.plotly_chart(fig1, use_container_width=True)

with col6:
    fig2 = px.histogram(df, x="Total_runs", nbins=30, title="Runs Distribution per Match", color_discrete_sequence=["#f95d6a"])
    st.plotly_chart(fig2, use_container_width=True)

col7, col8 = st.columns(2)

with col7:
    top_batters = df.groupby("Batter")["Batter_runs"].sum().reset_index().sort_values(by="Batter_runs", ascending=False).head(10)
    fig3 = px.bar(top_batters, x="Batter_runs", y="Batter", orientation="h", title="Top 10 Run Scorers", color="Batter_runs")
    st.plotly_chart(fig3, use_container_width=True)

with col8:
    top_bowlers = df[df["Player_Out"].notna()].groupby("Bowler")["Player_Out"].count().reset_index().sort_values(by="Player_Out", ascending=False).head(10)
    top_bowlers.columns = ["Bowler", "Wickets"]
    fig4 = px.bar(top_bowlers, x="Wickets", y="Bowler", orientation="h", title="Top 10 Wicket Takers", color="Wickets")
    st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")
st.info("💡 Tip: Use the sidebar to explore other match types and customize visuals.")

