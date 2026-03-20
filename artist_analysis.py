#!/usr/bin/env python3
# full_artist_analysis_console.py

import pandas as pd
import numpy as np
import statsmodels.api as sm
import ast
import plotext as plt  # voor console plots

# --- Data inlezen ---
DATA_PATH = "artist_data.csv"
df = pd.read_csv(DATA_PATH)

# --- Part 1: Basic Inspection ---
print("=== Part 1: Basic Inspection of the Data ===")

print("\nColumns and data types:")
print(df.dtypes)

print("\nFirst 5 rows:")
print(df.head())

num_artists = df['name'].nunique()
print(f"\nNumber of unique artists: {num_artists}")

# Top 10 artists by popularity
top10_pop = df.nlargest(10, 'artist_popularity')[['name','artist_popularity']]
print("\n=== Top 10 Artists by Popularity ===")
print(top10_pop.to_string(index=False))

# Top 10 artists by number of genres
genre_cols = ['artist_genres','genre_1','genre_2','genre_3','genre_4','genre_5','genre_6']
df['num_genres'] = df[genre_cols].apply(lambda row: sum([1 for x in row if pd.notna(x)]), axis=1)
top10_genres = df.nlargest(10, 'num_genres')[['name','num_genres']]
print("\n=== Top 10 Artists by Number of Genres ===")
print(top10_genres.to_string(index=False))

# Console bar plots
print("\nBar chart: Top 10 Popularity")
plt.clear_figure()
plt.bar(top10_pop['name'].tolist(), top10_pop['artist_popularity'].tolist())
plt.show()

print("\nBar chart: Top 10 Number of Genres")
plt.clear_figure()
plt.bar(top10_genres['name'].tolist(), top10_genres['num_genres'].tolist())
plt.show()

# --- Part 2: Popularity vs Followers ---
print("\n=== Part 2: Popularity vs Followers ===")
df['followers'] = pd.to_numeric(df['followers'].astype(str).str.replace(",",""), errors="coerce").fillna(0)
df_clean = df[df['followers'] > 0].copy()
df_clean['log_followers'] = np.log(df_clean['followers'])

X = sm.add_constant(df_clean['log_followers'])
y = df_clean['artist_popularity']
model = sm.OLS(y, X).fit()
print("\n=== Linear Regression Summary ===")
print(model.summary())

df_clean['pred'] = model.predict(X)
df_clean['residual'] = df_clean['artist_popularity'] - df_clean['pred']

print("\nTop 10 Overperformers:")
print(df_clean.nlargest(10,'residual')[['name','artist_popularity','followers','residual']].to_string(index=False))

print("\nTop 10 Legacy Artists:")
print(df_clean.nsmallest(10,'residual')[['name','artist_popularity','followers','residual']].to_string(index=False))

# Scatter plot console
print("\nScatter plot: Popularity vs Log(Followers)")
plt.clear_figure()
plt.scatter(df_clean['log_followers'].tolist(), df_clean['artist_popularity'].tolist())
plt.show()

# --- Part 3: Genre Analysis ---
print("\n=== Part 3: Genre Analysis ===")
def parse_genres_cell(cell):
    if pd.isna(cell):
        return []
    try:
        val = ast.literal_eval(cell)
        if isinstance(val, (list, tuple)):
            return [str(x).strip() for x in val]
    except Exception:
        pass
    return [p.strip() for p in str(cell).split(',') if p.strip()]

df['genres_parsed'] = df['artist_genres'].apply(parse_genres_cell)

def top_artists_by_genre(df, genre):
    mask = df['genres_parsed'].apply(lambda genres: genre.lower() in [g.lower() for g in genres])
    df_genre = df[mask].sort_values('artist_popularity', ascending=False)
    print(f"\nTop 10 artists in genre '{genre}':")
    print(df_genre[['name','artist_popularity','followers']].head(10).to_string(index=False))

top_artists_by_genre(df,'pop')

# --- Part 4: Number of Genres vs Popularity/Followers ---
print("\n=== Part 4: Number of Genres vs Popularity/Followers ===")
plt.clear_figure()
plt.scatter(df['num_genres'].tolist(), df['artist_popularity'].tolist(), label='Popularity')
plt.scatter(df['num_genres'].tolist(), df['followers'].tolist(), label='Followers')
plt.title("Number of Genres vs Popularity & Followers")
plt.show()

print("\nHistogram: Number of Genres per Artist")
plt.clear_figure()
plt.hist(df['num_genres'].tolist(), bins=range(0, df['num_genres'].max()+2))
plt.show()
