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
