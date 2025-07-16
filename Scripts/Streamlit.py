# --- Imports ---
import streamlit as st
import pandas as pd
import base64
import plotly.express as px
import mysql.connector

# --- SQL Connection ---

def get_connection():
    try:
        return mysql.connector.connect(
            host="localhost",       
            user="root",   
            password="123456789", 
            database="cric_sheet_db"
        )
    except mysql.connector.Error as err:
        st.error(f"Database connection failed: {err}")
        return None

# --- Table Mapping ---

TABLE_MAPPING = {
    "IPL": "ipl_matches",
    "ODI": "odi_matches",
    "T20I": "t20_matches",
    "TEST": "test_matches"
}

# --- Load Data from SQL ---
@st.cache_data
def load_sql_data(match_type):
    table_name = TABLE_MAPPING.get(match_type)
    if not table_name:
        st.error(f"No table mapping found for match type: {match_type}")
        return pd.DataFrame()
    
    query = f"SELECT * FROM {table_name}"
    conn = get_connection()
    if not conn:
        return pd.DataFrame()

    try:
        df = pd.read_sql(query, conn)
        if "Date" in df.columns:
            df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
            df["Year"] = df["Date"].dt.year
        return df
    except Exception as e:
        st.error(f"Failed to fetch data: {e}")
        return pd.DataFrame()
    finally:
        conn.close()

# --- Convert Image to Base64 ---
def img_to_base64(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        return None

# --- Background Image Setup ---
IMAGE_PATH = "Image/Cricpic.jpg"
img_base64 = img_to_base64(IMAGE_PATH)
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

# --- Sidebar Selection ---
st.sidebar.title("🔍 Explore Formats")
match_types = ["IPL", "ODI", "T20I", "TEST"]
selected_format = st.sidebar.radio("Select Match Type", match_types)

# --- Load Match Data ---
df = load_sql_data(selected_format)

# --- Metrics & Visualizations ---
if not df.empty:
    st.markdown("## 🧾 Quick Overview")
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("🏏 Total Matches", df["Match_Number"].nunique() if "Match_Number" in df.columns else len(df))
    col2.metric("👥 Teams", df["Teams_Participated"].nunique() if "Teams_Participated" in df.columns else "N/A")
    col3.metric("📍 Venues", df["Venue"].nunique() if "Venue" in df.columns else "N/A")
    col4.metric("📆 Seasons", df["Season"].nunique() if "Season" in df.columns else "N/A")

    st.markdown("---")
    st.markdown("## 📊 Key Insights")
    col5, col6 = st.columns(2)

    with col5:
        if "Year" in df.columns:
            matches_per_year = df["Year"].value_counts().sort_index().reset_index()
            matches_per_year.columns = ["Year", "Matches"]
            fig1 = px.bar(matches_per_year, x="Year", y="Matches", title="Matches Per Year", color="Matches")
            st.plotly_chart(fig1, use_container_width=True)

    with col6:
        if "Total_runs" in df.columns:
            fig2 = px.histogram(df, x="Total_runs", nbins=30, title="Runs Distribution per Match", color_discrete_sequence=["#f95d6a"])
            st.plotly_chart(fig2, use_container_width=True)

    col7, col8 = st.columns(2)

    with col7:
        if "Batter" in df.columns and "Batter_runs" in df.columns:
            top_batters = df.groupby("Batter")["Batter_runs"].sum().reset_index().sort_values(by="Batter_runs", ascending=False).head(10)
            fig3 = px.bar(top_batters, x="Batter_runs", y="Batter", orientation="h", title="Top 10 Run Scorers", color="Batter_runs")
            st.plotly_chart(fig3, use_container_width=True)

    with col8:
        if "Bowler" in df.columns and "Player_Out" in df.columns:
            top_bowlers = df[df["Player_Out"].notna()].groupby("Bowler")["Player_Out"].count().reset_index().sort_values(by="Player_Out", ascending=False).head(10)
            top_bowlers.columns = ["Bowler", "Wickets"]
            fig4 = px.bar(top_bowlers, x="Wickets", y="Bowler", orientation="h", title="Top 10 Wicket Takers", color="Wickets")
            st.plotly_chart(fig4, use_container_width=True)

    st.markdown("---")
    st.info("💡 Tip: Use the sidebar to explore other match types and customize visuals.")
else:
    st.warning("⚠️ No data available for the selected match type.")
