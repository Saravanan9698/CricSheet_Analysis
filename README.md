# 🌟 CricSheet Analysis

Welcome to **CricSheet Analysis**, a comprehensive project designed to transform raw cricket match data into interactive, insightful, and visually appealing analytics. This project leverages data from [Cricsheet](https://cricsheet.org/) to provide detailed player performance metrics, match insights, and team statistics across various cricket formats (ODI, T20, and Test). Whether you're a cricket enthusiast, analyst, or strategist, this tool makes exploring cricket data intuitive and engaging.

---

## 📋 Project Overview

In the past, cricket fans and analysts relied on static scorecards and limited data for insights. **CricSheet Analysis** changes that by offering:
- **Structured Data Storage**: Efficiently organized data in MySQL for seamless querying.
- **SQL-Powered Insights**: Over 20 SQL queries to extract meaningful metrics like player stats, match outcomes, and team performance.
- **Exploratory Data Analysis (EDA)**: Rich visualizations using Python libraries (Matplotlib, Seaborn, Plotly) to uncover trends and patterns.
- **Interactive Dashboards**: A Power BI dashboard and Streamlit applications for dynamic, user-friendly data exploration.

This project combines web scraping, data preprocessing, and advanced visualization to enhance the cricket viewing experience and provide actionable insights.

---

## ✨ Key Features

- **Data Storage**: Structured MySQL tables for fast and reliable querying.
- **SQL Analysis**: Extensive queries to analyze player performance, match results, and team statistics.
- **EDA Visualizations**: Interactive and static plots using Matplotlib, Seaborn, and Plotly to highlight key trends.
- **Power BI Dashboard**: A visually rich, interactive dashboard for exploring match and player data.
- **Streamlit Applications**: Web-based apps for table views, custom queries, and visualizations.

---

## 🛠️ Technology Stack

| **Category**            | **Tools**                              |
|-------------------------|----------------------------------------|
| **Database**            | MySQL                                 |
| **Query Language**      | SQL                                   |
| **Data Analysis & EDA** | Python (Pandas, Matplotlib, Seaborn, Plotly) |
| **Data Visualization**  | Power BI, Streamlit                   |

---

## 📁 Project Structure

The project is organized into several folders and files, each serving a specific purpose:

### 1. 📂 **Raw JSON Files**
   - Contains raw JSON files from Cricsheet, converted to `.csv` format using Pandas for easier processing.

### 2. 📂 **General Datasets**
   - Stores general match information (e.g., teams, dates, venues) to support further analysis.

### 3. 📂 **Innings Datasets**
   - Includes detailed innings-level data used for plotting and in-depth analysis.

### 4. 📂 **Preprocessed General Datasets**
   - Processed versions of General Datasets, cleaned for null values and standardized date formats.

### 5. 📂 **Preprocessed Innings Datasets**
   - Cleaned innings data, with null values handled for consistency.

### 6. 📂 **Pages**
   - Contains Streamlit application files:
     - **Table View**: Displays data in tabular format.
     - **Query View**: Allows users to run custom SQL queries.
     - **Visualizations**: Interactive plots for data exploration.

### 7. 📂 **Scripts**
   - Python scripts for:
     - Extracting data from JSON files.
     - Converting JSON to CSV.
     - Preprocessing data.
     - Generating visualizations.

### 8. 📄 **Cricsheet.pbix**
   - A Power BI file hosting an interactive dashboard for intuitive match and player analysis.

---

## 🚀 Getting Started

### Prerequisites
- **MySQL**: For storing and querying data.
- **Python**: Install required libraries (`pandas`, `matplotlib`, `seaborn`, `plotly`, `streamlit`).
- **Power BI Desktop**: To view and interact with the `Cricsheet.pbix` dashboard.
- **Streamlit**: To run the web-based applications.

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/cricsheet-analysis.git
