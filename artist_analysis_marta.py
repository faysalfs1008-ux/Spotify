import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm

df = pd.read_csv("artist_data.csv")

# Inspecting Data
print(df.head())

print("\nColumns:")
print(df.columns)

print("\nData types:")
print(df.dtypes)

print("\nNumber of rows:", len(df))

# Counting Unique Artists
unique_artists = df["name"].nunique()
print("Number of unique artists:", unique_artists)

# Top 10 By Popularity
top_popularity = df.sort_values("artist_popularity", ascending=False).head(10)

plt.figure(figsize=(10,6))
sns.barplot(x="artist_popularity", y="name", data=top_popularity)
plt.title("Top 10 Artists by Popularity")
plt.xlabel("Popularity")
plt.ylabel("Artist")
plt.tight_layout()
plt.show()

# Top 10 By Followers
top_followers = df.sort_values("followers", ascending=False).head(10)

plt.figure(figsize=(10,6))
sns.barplot(x="followers", y="name", data=top_followers)
plt.title("Top 10 Artists by Followers")
plt.xlabel("Followers")
plt.ylabel("Artist")
plt.tight_layout()
plt.show()

# Popularity vs Followers
df["log_followers"] = np.log(df["followers"] + 1)

plt.figure(figsize=(8,6))
sns.scatterplot(x="log_followers", y="artist_popularity", data=df)
plt.title("Popularity vs Log(Followers)")
plt.xlabel("Log Followers")
plt.ylabel("Popularity")
plt.show()

corr = df["artist_popularity"].corr(df["log_followers"])
print("Correlation between popularity and log followers:", corr)

X = sm.add_constant(df["log_followers"])
y = df["artist_popularity"]

model = sm.OLS(y, X).fit()

print(model.summary())

# Over-performers and Legacy Artists
df["predicted_popularity"] = model.predict(X)
df["residual"] = df["artist_popularity"] - df["predicted_popularity"]

overperformers = df.sort_values("residual", ascending=False).head(10)
legacy_artists = df.sort_values("residual", ascending=True).head(10)

print("\nTop 10 over-performing artists:")
print(overperformers[["name", "artist_popularity", "followers", "predicted_popularity", "residual"]])

print("\nTop 10 legacy artists:")
print(legacy_artists[["name", "artist_popularity", "followers", "predicted_popularity", "residual"]])

# Top Artists By Genre
genre_columns = ["genre_0","genre_1","genre_2","genre_3","genre_4","genre_5","genre_6"]

def top_artists_by_genre(genre):

    mask = False

    for col in genre_columns:
        mask = mask | df[col].astype(str).str.contains(genre, case=False, na=False)

    filtered = df[mask]

    top = filtered.sort_values("artist_popularity", ascending=False).head(10)

    print(top[["name","artist_popularity","followers"]])

top_artists_by_genre("classic rock")

# Number of Genres Correlations
genre_columns = ["genre_0", "genre_1", "genre_2", "genre_3", "genre_4", "genre_5", "genre_6"]

df["num_genres"] = 1 + df[genre_columns].apply(
    lambda row: sum(pd.notna(row) & (row.astype(str).str.strip() != "")),
    axis=1
)

print("\nSummary of num_genres:")
print(df["num_genres"].describe())

# Number of Genres per Artist
genre_counts = df["num_genres"].value_counts().sort_index()

plt.figure(figsize=(8, 6))
sns.barplot(x=genre_counts.index, y=genre_counts.values)
plt.title("Number of Genres per Artist")
plt.xlabel("Number of Genres")
plt.ylabel("Count")
plt.xticks(range(len(genre_counts.index)), genre_counts.index)
plt.tight_layout()
plt.show()


# Correlation With Popularity and Followers
print("\nCorrelation with popularity:",
      df["num_genres"].corr(df["artist_popularity"]))

print("Correlation with followers:",
      df["num_genres"].corr(df["followers"]))

# Artist Popularity by Number of Genres
plt.figure(figsize=(8, 6))
sns.boxplot(x="num_genres", y="artist_popularity", data=df)
plt.title("Artist Popularity by Number of Genres")
plt.xlabel("Number of Genres")
plt.ylabel("Artist Popularity")
plt.tight_layout()
plt.show()

# Additional Insights
all_genre_columns = ["genre_0", "genre_1", "genre_2", "genre_3", "genre_4", "genre_5", "genre_6"]

all_genres = pd.concat([df[col] for col in all_genre_columns], ignore_index=True)

all_genres = all_genres.dropna().astype(str).str.strip()

top_genres = all_genres.value_counts().head(10)

print(top_genres)

plt.figure(figsize=(10, 6))
sns.barplot(x=top_genres.values, y=top_genres.index)
plt.title("Most Common Genres")
plt.xlabel("Number of Artists")
plt.ylabel("Genre")
plt.tight_layout()
plt.show()

