import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm

df = pd.read_csv("artist_data.csv")


# Basic inspection

print("First 5 rows:")
print(df.head())

print("\nColumns:")
print(df.columns.tolist())

print("\nData types:")
print(df.dtypes)

print("\nNumber of rows:", len(df))
print("Number of unique artists:", df["name"].nunique())

# Clean data for analysis

df = df.dropna(subset=["artist_popularity", "followers"]).copy()
df["log_followers"] = np.log(df["followers"] + 1)

genre_columns = ["genre_0", "genre_1", "genre_2", "genre_3", "genre_4", "genre_5", "genre_6"]

# Count non-empty genres per artist
df["num_genres"] = df[genre_columns].apply(
    lambda row: ((pd.notna(row)) & (row.astype(str).str.strip() != "")).sum(),
    axis=1
)

# Top 10 artists by popularity

top_popularity = df.sort_values("artist_popularity", ascending=False).head(10)

plt.figure(figsize=(10, 6))
sns.barplot(data=top_popularity, x="artist_popularity", y="name")
plt.title("Top 10 Artists by Popularity")
plt.xlabel("Popularity")
plt.ylabel("Artist")
plt.tight_layout()
plt.show()

 
# Top 10 artists by followers

top_followers = df.sort_values("followers", ascending=False).head(10)

plt.figure(figsize=(10, 6))
sns.barplot(data=top_followers, x="followers", y="name")
plt.title("Top 10 Artists by Followers")
plt.xlabel("Followers")
plt.ylabel("Artist")
plt.tight_layout()
plt.show()

# Popularity vs followers

plt.figure(figsize=(8, 6))
sns.scatterplot(data=df, x="log_followers", y="artist_popularity", alpha=0.6)
plt.title("Artist Popularity vs Log(Followers)")
plt.xlabel("Log(Followers + 1)")
plt.ylabel("Artist Popularity")
plt.tight_layout()
plt.show()

corr = df["artist_popularity"].corr(df["log_followers"])
print("\nCorrelation between artist popularity and log followers:", corr)

X = sm.add_constant(df["log_followers"])
y = df["artist_popularity"]

model = sm.OLS(y, X).fit()
print("\nOLS Regression Results:")
print(model.summary())

# Over-performers and legacy artists
# Residual > 0  => more popular than expected
# Residual < 0  => less popular than expected

df["predicted_popularity"] = model.predict(X)
df["residual"] = df["artist_popularity"] - df["predicted_popularity"]

overperformers = df.sort_values("residual", ascending=False).head(10)
legacy_artists = df.sort_values("residual", ascending=True).head(10)

print("\nTop 10 over-performing artists:")
print(overperformers[["name", "artist_popularity", "followers", "predicted_popularity", "residual"]])

print("\nTop 10 legacy artists:")
print(legacy_artists[["name", "artist_popularity", "followers", "predicted_popularity", "residual"]])

# Function: top artists by genre

def top_artists_by_genre(genre: str) -> pd.DataFrame:
    mask = pd.Series(False, index=df.index)

    for col in genre_columns:
        mask = mask | df[col].astype(str).str.contains(genre, case=False, na=False)

    filtered = df[mask]
    top = filtered.sort_values("artist_popularity", ascending=False).head(10)

    return top[["name", "artist_popularity", "followers"]]

print("\nTop artists in genre 'classic rock':")
print(top_artists_by_genre("classic rock"))

# Number of genres per artist

print("\nSummary of number of genres:")
print(df["num_genres"].describe())

genre_counts = df["num_genres"].value_counts().sort_index()

plt.figure(figsize=(8, 6))
sns.barplot(x=genre_counts.index, y=genre_counts.values)
plt.title("Number of Genres per Artist")
plt.xlabel("Number of Genres")
plt.ylabel("Number of Artists")
plt.tight_layout()
plt.show()

# Correlation of number of genres
# with popularity and followers

print("\nCorrelation between number of genres and popularity:",
      df["num_genres"].corr(df["artist_popularity"]))

print("Correlation between number of genres and followers:",
      df["num_genres"].corr(df["followers"]))

print("Correlation between number of genres and log followers:",
      df["num_genres"].corr(df["log_followers"]))

plt.figure(figsize=(8, 6))
sns.boxplot(data=df, x="num_genres", y="artist_popularity")
plt.title("Artist Popularity by Number of Genres")
plt.xlabel("Number of Genres")
plt.ylabel("Artist Popularity")
plt.tight_layout()
plt.show()

# Additional insight:
# most common genres

all_genres = pd.concat([df[col] for col in genre_columns], ignore_index=True)
all_genres = all_genres.dropna().astype(str).str.strip()
all_genres = all_genres[all_genres != ""]

top_genres = all_genres.value_counts().head(10)

print("\nTop 10 most common genres:")
print(top_genres)

plt.figure(figsize=(10, 6))
sns.barplot(x=top_genres.values, y=top_genres.index)
plt.title("Top 10 Most Common Genres")
plt.xlabel("Number of Artists")
plt.ylabel("Genre")
plt.tight_layout()
plt.show()