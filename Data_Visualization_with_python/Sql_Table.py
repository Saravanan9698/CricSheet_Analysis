# 📦 Importing Required Packages
import streamlit as st
import pandas as pd
import mysql.connector as db
from mysql.connector import Error
from datetime import datetime
import base64
import os

# 🚧 Page Configuration
st.set_page_config(page_title="Cricsheet DB Viewer", layout="wide")

# 🎨 Load and Apply Background Image
def apply_background(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as file:
            img_base64 = base64.b64encode(file.read()).decode()
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
    else:
        st.warning("⚠️ Background image not found.")

# 📡 Establish Database Connection
def create_connection():
    try:
        return db.connect(
            user='root',
            password='123456789',
            host='localhost',
            database='cric_sheet_db'
        )
    except Error as e:
        st.error(f"❌ Connection Failed: {e}")
        return None

# 📋 Retrieve Table Names
def get_table_names(conn):
    try:
        with conn.cursor() as cursor:
            cursor.execute("SHOW TABLES")
            return [table[0] for table in cursor.fetchall()]
    except Error as e:
        st.error(f"❌ Failed to fetch tables: {e}")
        return []

# 📥 Load Table Data
def fetch_table_data(conn, table_name):
    try:
        return pd.read_sql(f"SELECT * FROM `{table_name}`", conn)
    except Error as e:
        st.error(f"❌ Failed to fetch `{table_name}`: {e}")
        return None

# 🚀 Streamlit App
def main():
    apply_background(r"D:\Projects\Mini_Projects\CricSheet_Analysis\Image\Cric_pic_worldcup.jpg")
    st.title("🏏 Cricsheet MySQL Table Viewer")
    st.markdown("Easily explore and download cricket match datasets stored in MySQL.")

    conn = create_connection()
    MAX_ROWS = 1000

    if conn:
        tables = get_table_names(conn)
        if tables:
            selected_table = st.selectbox("📑 Select a Table", tables)

            if selected_table:
                df = fetch_table_data(conn, selected_table)
                if df is not None and not df.empty:
                    st.success(f"✅ Loaded `{selected_table}` — {df.shape[0]} rows × {df.shape[1]} columns")

                    selected_cols = st.multiselect(
                        "📌 Choose Columns to Display", df.columns.tolist(), default=df.columns.tolist()
                    )
                    df_filtered = df[selected_cols] if selected_cols else df

                    if len(df_filtered) > MAX_ROWS:
                        st.warning(f"⚠️ Table is large. Showing first {MAX_ROWS} rows.")
                        st.dataframe(df_filtered.head(MAX_ROWS), use_container_width=True)
                    else:
                        st.dataframe(df_filtered, use_container_width=True)

                    csv_data = df_filtered.to_csv(index=False).encode("utf-8")
                    file_name = f"{selected_table}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

                    st.download_button(
                        "⬇️ Download Filtered CSV",
                        data=csv_data,
                        file_name=file_name,
                        mime="text/csv"
                    )
                else:
                    st.error("❌ Table is empty or couldn't be loaded.")
        else:
            st.warning("⚠️ No tables found in the connected database.")

        conn.close()
    else:
        st.error("🚫 Failed to connect to MySQL.")

if __name__ == "__main__":
    main()