import streamlit as st
import pandas as pd
import mysql.connector as db
import base64

# Page configuration
st.set_page_config(page_title="Cricsheet Query View", layout="wide")

# Background image function
def img_to_base64(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        st.warning("Background image not found.")
        return None

# Set background
image_path = r"D:\Projects\Mini_Projects\CricSheet_Analysis\Image\cricket-batsman-2560x1440-17540.jpeg"
img_base64 = img_to_base64(image_path)
if img_base64:
    st.markdown(f"""
        <style>
        .stApp {{
            background-image: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)),
            url('data:image/jpeg;base64,{img_base64}');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        </style>
    """, unsafe_allow_html=True)

# Database connection
# @st.cache_resource  # Uncomment for performance boost
def get_connection():
    return db.connect(
        host='localhost',
        user='root',
        password='123456789',
        database='cric_sheet_db'
    )

connection = get_connection()

# SQL Queries and Titles
sql_queries = {
    # 🏏 Top 10 Batsmen
    'Top 10 Batsman in IPL Matches': "SELECT Batter AS Batsman, SUM(Total_runs) AS Runs FROM cric_sheet_db.ipl_matches GROUP BY Batsman ORDER BY Runs DESC LIMIT 10;",
    'Top 10 Batsman in ODI Matches': "SELECT Batter AS Batsman, SUM(Total_runs) AS Runs FROM cric_sheet_db.odi_matches GROUP BY Batsman ORDER BY Runs DESC LIMIT 10;",
    'Top 10 Batsman in T20 Matches': "SELECT Batter AS Batsman, SUM(Total_runs) AS Runs FROM cric_sheet_db.t20_matches GROUP BY Batsman ORDER BY Runs DESC LIMIT 10;",
    'Top 10 Batsman in TEST Matches': "SELECT Batter AS Batsman, SUM(Total_runs) AS Runs FROM cric_sheet_db.test_matches GROUP BY Batsman ORDER BY Runs DESC LIMIT 10;",

    # 🎯 Top 10 Bowlers
    'Leading wicket-takers in IPL Matches': "SELECT Bowler, COUNT(Type) AS Wickets FROM cric_sheet_db.ipl_matches WHERE Type IS NOT NULL GROUP BY Bowler ORDER BY Wickets DESC LIMIT 10;",
    'Leading wicket-takers in ODI Matches': "SELECT Bowler, COUNT(Type) AS Wickets FROM cric_sheet_db.odi_matches WHERE Type IS NOT NULL GROUP BY Bowler ORDER BY Wickets DESC LIMIT 10;",
    'Leading wicket-takers in T20 Matches': "SELECT Bowler, COUNT(Type) AS Wickets FROM cric_sheet_db.t20_matches WHERE Type IS NOT NULL GROUP BY Bowler ORDER BY Wickets DESC LIMIT 10;",
    'Leading wicket-takers in TEST Matches': "SELECT Bowler, COUNT(Type) AS Wickets FROM cric_sheet_db.test_matches WHERE Type IS NOT NULL GROUP BY Bowler ORDER BY Wickets DESC LIMIT 10;",

    # 🏟️ Most Played Venues
    'Top 10 Venues in IPL Matches': "SELECT Venue, COUNT(DISTINCT Match_Number) AS Matches FROM cric_sheet_db.ipl_matches GROUP BY Venue ORDER BY Matches DESC LIMIT 10;",
    'Top 10 Venues in ODI Matches': "SELECT Venue, COUNT(DISTINCT Match_Number) AS Matches FROM cric_sheet_db.odi_matches GROUP BY Venue ORDER BY Matches DESC LIMIT 10;",
    'Top 10 Venues in T20 Matches': "SELECT Venue, COUNT(DISTINCT Match_Number) AS Matches FROM cric_sheet_db.t20_matches GROUP BY Venue ORDER BY Matches DESC LIMIT 10;",
    'Top 10 Venues in TEST Matches': "SELECT Venue, COUNT(DISTINCT Match_Number) AS Matches FROM cric_sheet_db.test_matches GROUP BY Venue ORDER BY Matches DESC LIMIT 10;",

    # 🏆 Most Match Wins
    'Most Match Wins in IPL': "SELECT Match_Winner, COUNT(DISTINCT Match_Number) AS Wins FROM cric_sheet_db.ipl_matches WHERE Match_Winner IS NOT NULL GROUP BY Match_Winner ORDER BY Wins DESC LIMIT 10;",
    'Most Match Wins in ODI': "SELECT Match_Winner, COUNT(DISTINCT Match_Number) AS Wins FROM cric_sheet_db.odi_matches WHERE Match_Winner IS NOT NULL GROUP BY Match_Winner ORDER BY Wins DESC LIMIT 10;",
    'Most Match Wins in T20': "SELECT Match_Winner, COUNT(DISTINCT Match_Number) AS Wins FROM cric_sheet_db.t20_matches WHERE Match_Winner IS NOT NULL GROUP BY Match_Winner ORDER BY Wins DESC LIMIT 10;",
    'Most Match Wins in TEST': "SELECT Match_Winner, COUNT(DISTINCT Match_Number) AS Wins FROM cric_sheet_db.test_matches WHERE Match_Winner IS NOT NULL GROUP BY Match_Winner ORDER BY Wins DESC LIMIT 10;",

    # 🧠 Man of the Match Awards
    'Top 10 Man of the Match in IPL': "SELECT Man_Of_Match, COUNT(DISTINCT Match_Number) AS Awards FROM cric_sheet_db.ipl_matches WHERE Man_Of_Match IS NOT NULL GROUP BY Man_Of_Match ORDER BY Awards DESC LIMIT 10;",
    'Top 10 Man of the Match in ODI': "SELECT Man_Of_Match, COUNT(DISTINCT Match_Number) AS Awards FROM cric_sheet_db.odi_matches WHERE Man_Of_Match IS NOT NULL GROUP BY Man_Of_Match ORDER BY Awards DESC LIMIT 10;",
    'Top 10 Man of the Match in T20': "SELECT Man_Of_Match, COUNT(DISTINCT Match_Number) AS Awards FROM cric_sheet_db.t20_matches WHERE Man_Of_Match IS NOT NULL GROUP BY Man_Of_Match ORDER BY Awards DESC LIMIT 10;",
    'Top 10 Man of the Match in TEST': "SELECT Man_Of_Match, COUNT(DISTINCT Match_Number) AS Awards FROM cric_sheet_db.test_matches WHERE Man_Of_Match IS NOT NULL GROUP BY Man_Of_Match ORDER BY Awards DESC LIMIT 10;",

    # 🧢 Toss Decision Trends
    'Toss Decision Trends in IPL': "SELECT Choose_To, COUNT(DISTINCT Match_Number) AS Matches FROM cric_sheet_db.ipl_matches GROUP BY Choose_To ORDER BY Matches DESC;",
    'Toss Decision Trends in ODI': "SELECT Choose_To, COUNT(DISTINCT Match_Number) AS Matches FROM cric_sheet_db.odi_matches GROUP BY Choose_To ORDER BY Matches DESC;",
    'Toss Decision Trends in T20': "SELECT Choose_To, COUNT(DISTINCT Match_Number) AS Matches FROM cric_sheet_db.t20_matches GROUP BY Choose_To ORDER BY Matches DESC;",
    'Toss Decision Trends in TEST': "SELECT Choose_To, COUNT(DISTINCT Match_Number) AS Matches FROM cric_sheet_db.test_matches GROUP BY Choose_To ORDER BY Matches DESC;",

    # 📊 Matches Per Season
    'Matches Per Season in IPL': "SELECT Season, COUNT(DISTINCT Match_Number) AS Matches FROM cric_sheet_db.ipl_matches GROUP BY Season ORDER BY Season;",
    'Matches Per Season in ODI': "SELECT Season, COUNT(DISTINCT Match_Number) AS Matches FROM cric_sheet_db.odi_matches GROUP BY Season ORDER BY Season;",
    'Matches Per Season in T20': "SELECT Season, COUNT(DISTINCT Match_Number) AS Matches FROM cric_sheet_db.t20_matches GROUP BY Season ORDER BY Season;",
    'Matches Per Season in TEST': "SELECT Season, COUNT(DISTINCT Match_Number) AS Matches FROM cric_sheet_db.test_matches GROUP BY Season ORDER BY Season;",
}

# UI
st.title("📊 Cricsheet Analytics Dashboard")
selected_title = st.selectbox("📌 Choose a Query to View:", list(sql_queries.keys()))

# Execute and display the selected query
query = sql_queries[selected_title]
try:
    df = pd.read_sql(query, connection)
    st.dataframe(df, use_container_width=True)
except Exception as e:
    st.error(f"Error running query: {e}")