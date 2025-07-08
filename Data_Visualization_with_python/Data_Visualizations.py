import streamlit as st
import pandas as pd
import base64
import plotly.express as px

# Load datasets
df_dict = {
    "IPL": pd.read_csv(r"D:\Projects\Mini_Projects\CricSheet_Analysis\CSV_Datasets\ipl_json_combined_cleaned.csv"),
    "ODI": pd.read_csv(r"D:\Projects\Mini_Projects\CricSheet_Analysis\CSV_Datasets\odis_json_combined_cleaned.csv"),
    "T20": pd.read_csv(r"D:\Projects\Mini_Projects\CricSheet_Analysis\CSV_Datasets\t20s_json_combined_cleaned.csv"),
    "TEST": pd.read_csv(r"D:\Projects\Mini_Projects\CricSheet_Analysis\CSV_Datasets\tests_json_combined_cleaned.csv"),
}

# Set page config
st.set_page_config(page_title="Cricsheet Analytics", layout="wide")

# Background image
def img_to_base64(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        return None

img_path = r"D:\Projects\Mini_Projects\CricSheet_Analysis\Image\cartoon-character-playing-cricket-game-field.jpg"
img_base64 = img_to_base64(img_path)
if img_base64:
    st.markdown(f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)),
                        url("data:image/jpg;base64,{img_base64}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        </style>
    """, unsafe_allow_html=True)

# Sidebar
st.sidebar.title("🏏 Cricsheet Match Types")
match_type = st.sidebar.selectbox("Select Format", list(df_dict.keys()))

# Load selected dataset
df = df_dict[match_type]

# Extract Year if not present
if "Year" not in df.columns:
    try:
        df["Date"] = pd.to_datetime(df["Date"], errors='coerce')
        df["Year"] = df["Date"].dt.year
    except Exception as e:
        st.error(f"Could not extract Year from Date: {e}")
        df["Year"] = None

st.title(f"📊 {match_type} Cricket Data Analysis")

# Visual Functions
def plot_match_winners():
    winners = df["Match_Winner"].value_counts().reset_index()
    winners.columns = ["Team", "Wins"]
    fig = px.bar(winners, x="Wins", y="Team", color="Team", title="Match Winners Count")
    st.plotly_chart(fig, use_container_width=True)

def plot_toss_decisions():
    fig = px.histogram(df, y="Choose_To", color="Choose_To", title="Toss Decisions")
    st.plotly_chart(fig, use_container_width=True)

def plot_top_batsmen():
    top_bat = df.groupby("Batter")["Batter_runs"].sum().reset_index()
    top_bat = top_bat.sort_values(by="Batter_runs", ascending=False).head(15)
    fig = px.bar(top_bat, x="Batter_runs", y="Batter", color="Batter", title="Top 15 Run Scorers")
    st.plotly_chart(fig, use_container_width=True)

def plot_top_bowlers():
    top_bowl = df[df["Player_Out"].notna()].groupby("Bowler")["Player_Out"].count().reset_index()
    top_bowl.columns = ["Bowler", "Wickets"]
    top_bowl = top_bowl.sort_values(by="Wickets", ascending=False).head(15)
    fig = px.bar(top_bowl, x="Wickets", y="Bowler", color="Bowler", title="Top 15 Wicket Takers")
    st.plotly_chart(fig, use_container_width=True)

def plot_runs_by_year():
    if df["Year"].isnull().all():
        st.warning("Year data is missing or invalid for this format.")
        return
    runs_year = df.groupby("Year")["Total_runs"].sum().reset_index()
    fig = px.line(runs_year, x="Year", y="Total_runs", markers=True, title="Total Runs per Year")
    st.plotly_chart(fig, use_container_width=True)

def plot_toss_by_team():
    tosses = df.groupby("Toss_Winner")["Choose_To"].value_counts().unstack().fillna(0)
    tosses = tosses.reset_index().melt(id_vars="Toss_Winner", var_name="Decision", value_name="Count")
    fig = px.bar(tosses, x="Toss_Winner", y="Count", color="Decision", barmode="group", title="Toss Decision by Team")
    st.plotly_chart(fig, use_container_width=True)

# Display visualizations
col1, col2 = st.columns(2)
with col1:
    plot_match_winners()
with col2:
    plot_toss_decisions()

col3, col4 = st.columns(2)
with col3:
    plot_top_batsmen()
with col4:
    plot_top_bowlers()

st.markdown("---")
col5, col6 = st.columns(2)
with col5:
    plot_runs_by_year()
with col6:
    plot_toss_by_team()