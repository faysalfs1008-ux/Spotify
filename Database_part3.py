import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Connect to database
conn = sqlite3.connect("spotify_database.db")
print("tracks_data schema:")
print(pd.read_sql("PRAGMA table_info(tracks_data);", conn))

# Reusable functions for dashboard

def get_explicit_popularity_data(conn):
    query = """
    SELECT 
        explicit,
        COUNT(*) AS number_of_tracks,
        AVG(track_popularity) AS average_popularity
    FROM tracks_data
    GROUP BY explicit
    """
    df = pd.read_sql(query, conn)
    df["explicit_label"] = df["explicit"].astype(str).replace({
        "false": "Non-explicit",
        "true": "Explicit"
    })
    return df


def get_collaboration_data(conn):
    query = """
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
        AVG(t.track_popularity) AS average_popularity
    FROM tracks_data t
    JOIN track_artist_counts tac
        ON t.id = tac.track_id
    GROUP BY collaboration
    """
    df = pd.read_sql(query, conn)
    df["collaboration_label"] = df["collaboration"].map({0: "Solo", 1: "Collaboration"})
    return df


def get_album_artist_popularity_data(conn):
    query = """
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
    return pd.read_sql(query, conn)


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
explicit_df = get_explicit_popularity_data(conn)

print("\nExplicit vs non-explicit tracks:")
print(explicit_df)

plt.figure(figsize=(8, 6))
sns.barplot(data=explicit_df, x="explicit_label", y="average_popularity")
plt.title("Average Popularity of Explicit vs Non-Explicit Tracks")
plt.xlabel("Track Type")
plt.ylabel("Average Popularity")
plt.tight_layout()
plt.show()

explicit_df.to_csv("explicit_popularity.csv", index=False)

print("\nConclusion: This analysis shows whether explicit tracks are on average more popular than non-explicit tracks.")

# 2. Which artists have the highest proportion of explicit tracks?
explicit_artist_query = """
SELECT 
    ar.name AS artist_name,
    COUNT(*) AS total_tracks,
    SUM(CASE WHEN LOWER(CAST(t.explicit AS TEXT)) = 'true' THEN 1 ELSE 0 END) AS explicit_tracks,
    CAST(SUM(CASE WHEN LOWER(CAST(t.explicit AS TEXT)) = 'true' THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) AS explicit_ratio
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

explicit_artist_df.to_csv("explicit_artist_ratio.csv", index=False)

print("\nConclusion: This shows which artists most frequently release explicit tracks, while excluding artists with too few tracks.")

# 3. Are collaborations more popular?
collaboration_df = get_collaboration_data(conn)

print("\nCollaboration vs solo tracks:")
print(collaboration_df)

plt.figure(figsize=(8, 6))
sns.barplot(data=collaboration_df, x="collaboration_label", y="average_popularity")
plt.title("Average Popularity of Collaboration vs Solo Tracks")
plt.xlabel("Track Type")
plt.ylabel("Average Popularity")
plt.tight_layout()
plt.show()

collaboration_df.to_csv("collaboration_popularity.csv", index=False)

print("\nConclusion: This analysis helps determine whether tracks with multiple artists perform better than solo tracks.")

# 4. Relationship between album popularity and artist popularity
album_artist_df = get_album_artist_popularity_data(conn)

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

album_artist_df.to_csv("album_artist_popularity.csv", index=False)

print("\nConclusion: This shows whether more popular artists also tend to have more popular albums.")

# 5. Album era column
era_query = """
SELECT
    *,
    CASE
        WHEN CAST(substr(release_date, 1, 4) AS INTEGER) BETWEEN 1970 AND 1979 THEN '70s'
        WHEN CAST(substr(release_date, 1, 4) AS INTEGER) BETWEEN 1980 AND 1989 THEN '80s'
        WHEN CAST(substr(release_date, 1, 4) AS INTEGER) BETWEEN 1990 AND 1999 THEN '90s'
        WHEN CAST(substr(release_date, 1, 4) AS INTEGER) BETWEEN 2000 AND 2009 THEN '00s'
        WHEN CAST(substr(release_date, 1, 4) AS INTEGER) BETWEEN 2010 AND 2019 THEN '10s'
        WHEN CAST(substr(release_date, 1, 4) AS INTEGER) >= 2020 THEN '20s'
        ELSE 'Unknown'
    END AS era
FROM albums_data
"""

albums_era_df = pd.read_sql(era_query, conn)

print("\nAlbums with era column:")
print(albums_era_df.head())

albums_era_df.to_csv("albums_with_era.csv", index=False)

print("\nConclusion: This adds an era category to albums so releases can be grouped by decade.")

# 6. Album-level feature analysis
print(pd.read_sql("""
SELECT album_name, COUNT(*) as tracks
FROM albums_data
GROUP BY album_name
ORDER BY tracks DESC
LIMIT 10;
""", conn))

chosen_album = "Exodus"

print(f"\nUsing album '{chosen_album}' because it has many tracks for meaningful analysis.")

album_features_query = """
SELECT
    al.album_name,
    al.track_name AS track_name,
    f.danceability,
    f.loudness,
    f.energy,
    f.valence
FROM albums_data al
JOIN tracks_data t
    ON al.track_id = t.id
JOIN features_data f
    ON t.id = f.id
WHERE al.album_name = ?
ORDER BY al.track_number
"""

album_features_df = pd.read_sql(album_features_query, conn, params=[chosen_album])

print(f"\nTrack features for album '{chosen_album}':")
print(album_features_df)

if not album_features_df.empty:
    plt.figure(figsize=(10, 6))
    sns.barplot(data=album_features_df, x="danceability", y="track_name")
    plt.title(f"Danceability Across Tracks on '{chosen_album}'")
    plt.xlabel("Danceability")
    plt.ylabel("Track")
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(10, 6))
    sns.barplot(data=album_features_df, x="loudness", y="track_name")
    plt.title(f"Loudness Across Tracks on '{chosen_album}'")
    plt.xlabel("Loudness")
    plt.ylabel("Track")
    plt.tight_layout()
    plt.show()
else:
    print(f"\nNo tracks found for album '{chosen_album}'. Please choose an existing album.")

album_features_df.to_csv("album_features_analysis.csv", index=False)

print("\nConclusion: This investigates how track features vary across one chosen album.")

# 7. Choose a feature and filter on top 10% tracks
top_feature_query = """
WITH ranked_tracks AS (
    SELECT
        f.id AS track_id,
        f.danceability,
        PERCENT_RANK() OVER (ORDER BY f.danceability) AS pct_rank
    FROM features_data f
),
top_tracks AS (
    SELECT
        track_id,
        danceability
    FROM ranked_tracks
    WHERE pct_rank >= 0.9
)
SELECT
    ar.name AS artist_name,
    COUNT(*) AS number_of_top_tracks,
    AVG(tt.danceability) AS average_danceability
FROM top_tracks tt
JOIN albums_data al
    ON tt.track_id = al.track_id
JOIN artist_data ar
    ON al.artist_id = ar.id
GROUP BY ar.name
ORDER BY number_of_top_tracks DESC, average_danceability DESC
LIMIT 10
"""

try:
    top_feature_df = pd.read_sql(top_feature_query, conn)

    print("\nArtists appearing most often in top 10% danceability tracks:")
    print(top_feature_df)

    plt.figure(figsize=(10, 6))
    sns.barplot(data=top_feature_df, x="number_of_top_tracks", y="artist_name")
    plt.title("Artists Appearing Most in Top 10% Danceability Tracks")
    plt.xlabel("Number of Top Tracks")
    plt.ylabel("Artist")
    plt.tight_layout()
    plt.show()

    top_feature_df.to_csv("top_danceability_artists.csv", index=False)

    print("\nConclusion: This analysis follows the assignment more closely by filtering the top 10% of tracks on a chosen feature and then checking which artists appear most often.")
except Exception as e:
    print("\nTop 10% feature analysis skipped.")
    print("Error details:", e)

# 8. Extra analysis: popularity by track duration group
duration_query = """
SELECT 
    CASE
        WHEN al.duration_ms < 180000 THEN 'Short (<3 min)'
        WHEN al.duration_ms BETWEEN 180000 AND 240000 THEN 'Medium (3-4 min)'
        ELSE 'Long (>4 min)'
    END AS duration_group,
    COUNT(*) AS number_of_tracks,
    AVG(t.track_popularity) AS average_popularity
FROM tracks_data t
JOIN albums_data al
    ON t.id = al.track_id
GROUP BY duration_group
ORDER BY average_popularity DESC
"""

try:
    duration_df = pd.read_sql(duration_query, conn)

    print("\nPopularity by track duration group:")
    print(duration_df)

    plt.figure(figsize=(8, 6))
    sns.barplot(data=duration_df, x="duration_group", y="average_popularity")
    plt.title("Average Popularity by Track Duration Group")
    plt.xlabel("Duration Group")
    plt.ylabel("Average Popularity")
    plt.tight_layout()
    plt.show()

    duration_df.to_csv("duration_popularity.csv", index=False)

    print("\nConclusion: This analysis explores whether shorter, medium-length, or longer tracks tend to be more popular.")
except Exception as e:
    print("\nDuration analysis skipped because the required column is not available in the current table.")
    print("Error details:", e)

print("\nPart 3 analysis completed successfully.")


# Close connection
conn.close()