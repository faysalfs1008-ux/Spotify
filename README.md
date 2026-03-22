# Spotify Data Analysis & Dashboard

This project analyzes Spotify data and presents insights through an interactive dashboard built using Streamlit. The dashboard allows users to explore artist statistics, track features, genre trends, and data-driven insights.

---

## Project Objectives

- Analyze Spotify track and artist data
- Investigate relationships between features such as danceability and popularity
- Explore trends over time and across genres
- Build an interactive dashboard to present findings

---
## Contributors 
- Marta Parada de Mingo

## Dataset

The script uses the following datasets:

- `artist_data.csv` – contains artist statistics, including:
  - `name` – artist name  
  - `artist_popularity` – popularity score (1–100)  
  - `followers` – number of followers  
  - `artist_genres`, `genre_1` … `genre_6` – artist genres  

> Ensure the CSV is in the same folder as the script.

---

## Features

1. **Basic Inspection**
   - Prints column names and types
   - Displays first 5 rows
   - Counts unique artists
   - Top 10 artists by popularity and number of genres (with bar charts)

2. **Popularity vs Followers**
   - Linear regression: `popularity ~ log(followers)`  
   - Identifies top overperformers (high popularity, low followers)  
   - Identifies top legacy artists (low popularity, high followers)  
   - Scatter plot with regression line

3. **Genre Analysis**
   - Parses genres from the dataset  
   - Function to show top 10 artists per genre (example: 'pop')  

4. **Number of Genres vs Popularity/Followers**
   - Scatter plot of number of genres vs popularity and followers  
   - Histogram showing distribution of genres per artist

---

## Requirements

Python 3 and the following packages are required:
pandas==2.2.0 
numpy==1.26.0 
matplotlib==3.8.0 
statsmodels==0.17.0
sqlite3==3.51.3
seaborn==0.13.2
