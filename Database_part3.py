import sqlite3
import pandas as pd

conn = sqlite3.connect("spotify_database.db")

tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", conn)
print(tables)

query1 = '''
SELECT explicit, AVG(popularity) as avg_popularity
FROM tracks_data
GROUP BY explicit
'''
print(pd.read_sql(query1, conn))

query2 = '''
SELECT t.track_id, t.popularity,
CASE WHEN COUNT(a.artist_id) > 1 THEN 1 ELSE 0 END as collaboration
FROM tracks_data t
JOIN albums_data al ON t.track_id = al.track_id
JOIN artist_data a ON al.artist_id = a.artist_id
GROUP BY t.track_id
'''
print(pd.read_sql(query2, conn).head())

query3 = '''
SELECT a.name, AVG(f.danceability) as avg_dance
FROM features_data f
JOIN tracks_data t ON f.track_id = t.track_id
JOIN albums_data al ON t.track_id = al.track_id
JOIN artist_data a ON al.artist_id = a.artist_id
GROUP BY a.name
ORDER BY avg_dance DESC
LIMIT 10
'''
print(pd.read_sql(query3, conn))
