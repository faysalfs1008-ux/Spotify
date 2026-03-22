# Spotify Data Analysis & Dashboard

This project analyzes Spotify data and presents insights through an interactive dashboard built using Streamlit. The dashboard allows users to explore artist statistics, track features, genre trends, and data-driven insights.

---

## Project Objectives

- Analyze Spotify track and artist data
- Investigate relationships between features such as danceability and popularity
- Explore trends over time and across genres
- Build an interactive dashboard to present findings

---

## Dashboard Features

The dashboard includes the following pages:

- **Home**
  - General statistics (number of artists, average popularity, followers)
  - Top artists visualization

- **Feature Analysis**
  - Distribution of selected features (danceability, energy)
  - Summary statistics

- **Genre Analysis**
  - Feature and popularity analysis by genre
  - Top artists within selected genre

- **Artist Search**
  - Search for artists by name
  - Displays popularity, followers, and genre

- **Insights**
  - Explicit vs non-explicit track popularity
  - Collaboration vs solo tracks
  - Artist vs album popularity relationship
  - Top danceability artists
  - Feature trends over time
  - Feature comparison by era
  
---

## Data Processing and Analysis

The project includes data analysis and preprocessing performed in earlier parts:

- Part 3: SQL-based analysis exported to CSV files (used in Insights page)
- Part 4: Data wrangling including cleaning, outlier detection, and time-based transformations

These results are integrated into the dashboard for visualization.

---

## Project Structure

The repository includes:

- `app.py` – main streamlit dashboard application
- `data_loader.py` – functions to load and process data
- `spotify_database.db` – SQLite database containing spotify data
- `.csv files` – results from analysis (Part 3)
- `data_wrangling_part4.py` – data cleaning and preparation

---

## How to Run

1. Install required packages:
   pip install streamlit pandas matplotlib seaborn sqlite3

2. Run the dashboard:
   streamlit run app.py

---

## Dataset

The project uses a SQLite database (`spotify_database.db`) containing:

- Track-level data (popularity, explicit, duration)
- Audio features (danceability, energy, tempo)
- Artist data (popularity, followers, genres)
- Album data (release dates)

Additional CSV files are generated from analysis and used in the Insights page.

---

## Group Members

- Marta Parada de Mingo – Dashboard development (Part 5)
- [Teammate 2] – Data analysis (Part 3)
- [Teammate 3] – Data wrangling (Part 4)

---
## Requirements

Python 3 and the following packages are required:
pandas==2.2.0 
numpy==1.26.0 
matplotlib==3.8.0 
statsmodels==0.17.0
sqlite3==3.51.3
seaborn==0.13.2

---

## Key Insights

- Explicit tracks tend to have higher average popularity
- Collaborative tracks perform better than solo tracks
- Artist popularity is positively correlated with album popularity
- Danceability has increased over time

---
