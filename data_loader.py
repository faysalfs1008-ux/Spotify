import pandas as pd

def get_artists_data():
    return pd.DataFrame({
        "artist_name": ["Taylor Swift", "Drake", "Bad Bunny", "The Weeknd", "Billie Eilish"],
        "popularity": [98, 96, 95, 97, 92],
        "followers": [120000000, 85000000, 78000000, 90000000, 65000000],
        "genres": ["pop", "hip hop", "latin", "r&b", "pop"],
        "year": [2023, 2023, 2023, 2023, 2023]
    })

def get_features_data():
    return pd.DataFrame({
        "track_name": ["Track A", "Track B", "Track C", "Track D", "Track E"],
        "danceability": [0.82, 0.71, 0.90, 0.66, 0.75],
        "energy": [0.79, 0.68, 0.88, 0.61, 0.70],
        "year": [2020, 2021, 2022, 2023, 2023],
        "genre": ["pop", "hip hop", "latin", "r&b", "pop"],
        "artist_name": ["Taylor Swift", "Drake", "Bad Bunny", "The Weeknd", "Billie Eilish"]
    })

def get_available_features(features_df):
    return ["danceability", "energy"]

def get_available_genres(features_df):
    return sorted(features_df["genre"].dropna().unique().tolist())