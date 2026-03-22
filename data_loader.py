import sqlite3
import pandas as pd

# Database connection
def get_connection():
    return sqlite3.connect("spotify_database.db")


# Artists data
def get_artists_data():
    conn = get_connection()

    query = """
    SELECT 
        name AS artist_name,
        artist_popularity AS popularity,
        followers
    FROM artist_data
    """

    df = pd.read_sql_query(query, conn)
    conn.close()

    return df


# Features data (joined tables)
def get_features_data():
    conn = get_connection()

    query = """
    SELECT 
        t.id,
        t.track_popularity AS popularity,
        t.explicit,
        f.danceability,
        f.energy,
        al.release_date,
        ar.name AS artist_name,
        ar.genre_0 AS genre
    FROM tracks_data t
    JOIN features_data f
        ON t.id = f.id
    JOIN albums_data al
        ON t.id = al.track_id
    JOIN artist_data ar
        ON al.artist_id = ar.id
    """

    df = pd.read_sql_query(query, conn)

    df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")
    df["year"] = df["release_date"].dt.year
    df = df.dropna(subset=["year"])

    df["genre"] = df["genre"].fillna("Unknown")

    conn.close()

    return df


# Feature
def get_available_features(features_df):
    return ["danceability", "energy"]

# Genre options
def get_available_genres(features_df):
    return sorted(features_df["genre"].dropna().unique().tolist())

# Era feature
def get_era_feature_data():
    features_df = get_features_data().copy()

    features_df["era"] = (features_df["year"] // 10) * 10

    era_data = (
        features_df.groupby("era")[["danceability", "energy"]]
        .mean()
        .reset_index()
        .sort_values("era")
    )
    return era_data

# Part 3 loaders

def load_explicit_popularity() :
    return pd.read_csv("explicit_popularity.csv")

def load_collaboration_popularity() :
    return pd.read_csv("collaboration_popularity.csv")

def load_album_artist_popularity() :
    return pd.read_csv("album_artist_popularity.csv")

def load_top_danceability_artists() :
    return pd.read_csv("top_danceability_artists.csv")

def load_explicit_artist_ratio() :
    return pd.read_csv("explicit_artist_ratio.csv")

def load_duration_popularity() :
    return pd.read_csv("duration_popularity.csv")

def load_albums_with_era() :
    return pd.read_csv("albums_with_era.csv")

def load_album_features_analysis() :
    return pd.read_csv("album_features_analysis.csv")
