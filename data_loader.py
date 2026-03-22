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

    df["genre"] = df["genre"].fillna("Unkown")

    conn.close()

    return df


# Feature
def get_available_features(features_df):
    return ["danceability", "energy"]

# Genre options
def get_available_genres(features_df):
    return sorted(features_df["genre"].dropna().unique().tolist())