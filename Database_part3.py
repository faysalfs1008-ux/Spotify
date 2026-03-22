import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Connect to database
conn = sqlite3.connect("spotify_database.db")

# Inspect available tables
tables_query = "SELECT name FROM sqlite_master WHERE type='table';"
tables = pd.read_sql(tables_query, conn)

print("Available tables:")
print(tables)

# Inspect columns per table
for table_name in tables["name"]:
    print(f"\nColumns in {table_name}:")
    info = pd.read_sql(f"PRAGMA table_info({table_name});", conn)
    print(info[["name", "type"]])

# 1. Are explicit tracks more popular?
explicit_query = """
SELECT 
    explicit,
    COUNT(*) AS number_of_tracks,
    AVG(popularity) AS average_popularity
FROM tracks_data
GROUP BY explicit
"""

explicit_df = pd.read_sql(explicit_query, conn)

print("\nExplicit vs non-explicit tracks:")
print(explicit_df)

plt.figure(figsize=(8, 6))
sns.barplot(data=explicit_df, x="explicit", y="average_popularity")
plt.title("Average Popularity of Explicit vs Non-Explicit Tracks")
plt.xlabel("Explicit")
plt.ylabel("Average Popularity")
plt.tight_layout()
plt.show()

# 2. Which artists have the highest proportion of explicit tracks?
explicit_artist_query = """
SELECT 
    ar.name AS artist_name,
    COUNT(*) AS total_tracks,
    SUM(CASE WHEN t.explicit = 1 THEN 1 ELSE 0 END) AS explicit_tracks,
    CAST(SUM(CASE WHEN t.explicit = 1 THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) AS explicit_ratio
FROM tracks_data t
JOIN albums_data al
    ON t.id = al.track_id
JOIN artist_data ar
    ON al.artist_id = ar.id
GROUP BY ar.name
HAVING COUNT(*) >= 5
ORDER BY explicit_ratio DESC, total_tracks DESC
LIMIT 10
"""

explicit_artist_df = pd.read_sql(explicit_artist_query, conn)

print("\nArtists with highest proportion of explicit tracks:")
print(explicit_artist_df)

plt.figure(figsize=(10, 6))
sns.barplot(data=explicit_artist_df, x="explicit_ratio", y="artist_name")
plt.title("Artists with Highest Proportion of Explicit Tracks")
plt.xlabel("Proportion of Explicit Tracks")
plt.ylabel("Artist")
plt.tight_layout()
plt.show()

# 3. Are collaborations more popular?
# A collaboration is a track with more than one artist
collaboration_query = """
WITH track_artist_counts AS (
    SELECT 
        al.track_id,
        COUNT(DISTINCT al.artist_id) AS artist_count
    FROM albums_data al
    GROUP BY al.track_id
)
SELECT 
    CASE 
        WHEN tac.artist_count > 1 THEN 1
        ELSE 0
    END AS collaboration,
    COUNT(*) AS number_of_tracks,
    AVG(t.popularity) AS average_popularity
FROM tracks_data t
JOIN track_artist_counts tac
    ON t.id = tac.track_id
GROUP BY collaboration
"""

collaboration_df = pd.read_sql(collaboration_query, conn)

print("\nCollaboration vs solo tracks:")
print(collaboration_df)

plt.figure(figsize=(8, 6))
sns.barplot(data=collaboration_df, x="collaboration", y="average_popularity")
plt.title("Average Popularity of Collaboration vs Solo Tracks")
plt.xlabel("Collaboration")
plt.ylabel("Average Popularity")
plt.tight_layout()
plt.show()

# 4. Relationship between album popularity and artist popularity
album_artist_query = """
SELECT 
    al.album_name,
    AVG(al.album_popularity) AS album_popularity,
    ar.name AS artist_name,
    ar.artist_popularity
FROM albums_data al
JOIN artist_data ar
    ON al.artist_id = ar.id
GROUP BY al.album_name, ar.name, ar.artist_popularity
"""

album_artist_df = pd.read_sql(album_artist_query, conn)

print("\nAlbum popularity vs artist popularity:")
print(album_artist_df.head())

plt.figure(figsize=(8, 6))
sns.scatterplot(
    data=album_artist_df,
    x="artist_popularity",
    y="album_popularity",
    alpha=0.5
)
plt.title("Album Popularity vs Artist Popularity")
plt.xlabel("Artist Popularity")
plt.ylabel("Album Popularity")
plt.tight_layout()
plt.show()

correlation = album_artist_df["artist_popularity"].corr(album_artist_df["album_popularity"])
print("\nCorrelation between artist popularity and album popularity:", correlation)

# 5. Top 10 artists for danceability
danceability_query = """
SELECT 
    ar.name AS artist_name,
    AVG(f.danceability) AS average_danceability,
    COUNT(*) AS number_of_tracks
FROM features_data f
JOIN tracks_data t
    ON f.id = t.id
JOIN albums_data al
    ON t.id = al.track_id
JOIN artist_data ar
    ON al.artist_id = ar.id
GROUP BY ar.name
HAVING COUNT(*) >= 5
ORDER BY average_danceability DESC
LIMIT 10
"""

danceability_df = pd.read_sql(danceability_query, conn)

print("\nTop 10 artists by average danceability:")
print(danceability_df)

plt.figure(figsize=(10, 6))
sns.barplot(data=danceability_df, x="average_danceability", y="artist_name")
plt.title("Top 10 Artists by Average Danceability")
plt.xlabel("Average Danceability")
plt.ylabel("Artist")
plt.tight_layout()
plt.show()

# Close connection
conn.close()