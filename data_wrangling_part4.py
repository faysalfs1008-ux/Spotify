#------------------------------------
# Part 4: Data Wrangling
# Task 1: Detect Outliers
#------------------------------------
import sqlite3
import pandas as pd

conn = sqlite3.connect("spotify_database.db")
tracks = pd.read_sql("SELECT * FROM tracks_data", conn)
artists = pd.read_sql("SELECT * FROM artist_data", conn)
albums = pd.read_sql("SELECT * FROM albums_data", conn)
features = pd.read_sql("SELECT * FROM features_data", conn)

df = tracks.merge(features, on='id')
df = df.merge(albums, left_on='id', right_on='track_id')
df = df.merge(artists, left_on='artist_id', right_on='id', suffixes=('', '_artist'))

print("Before cleaning:", df.shape)
print(df['energy'].describe())
print(df['tempo'].describe())

df = df[(df['tempo'] > 30) & (df['tempo'] < 220)]
print("After cleaning:", df.shape)
#----------------------------------
# Outlier Detection (IQR Method)
#------------------------------------
def find_outliers(df, col):
    # using IQR to find outliers
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1

    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    outliers = df[(df[col] < lower) | (df[col] > upper)]

    print("Outliers in", col, ":", len(outliers))
    print(outliers[col].head())  

    return outliers


outliers_energy = find_outliers(df, "energy")
outliers_tempo = find_outliers(df, "tempo")
outliers_danceability = find_outliers(df, "danceability")

#-----------------------------------
# Task 2: Check for invalid records
#------------------------------------
print("Missing track IDs:", df['id'].isnull().sum())
print("Missing artist IDs:", df['artist_id'].isnull().sum())

if 'duration_ms' in df.columns:
    print("Negative duration values:", (df['duration_ms'] < 0).sum())
print("Duplicate rows:", df.duplicated().sum())

df = df.dropna(subset=['id', 'artist_id'])
if 'duration_ms' in df.columns:
    df = df[df['duration_ms'] >= 0]

df = df.drop_duplicates()

df = df.dropna(axis=1, how='all')

print("After removing invalid records:", df.shape)

#-----------------------------------------
# Task 3: Prepare data for time analysis
#-----------------------------------------
df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
df['year'] = df['release_date'].dt.year

df = df.dropna(subset=['year'])

print("Data prepared for time analysis:", df[['release_date', 'year']].head())
# Analysis
features_over_time = df.groupby('year')[['energy', 'danceability', 'tempo']].mean().reset_index()

print("Average features over time:")
print(features_over_time.head())