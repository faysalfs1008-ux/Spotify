import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.api import OLS, add_constant

df = pd.read_csv("artist_data.csv")

print("Columns:", df.columns)
print(df.describe())
print("Unique artists:", df["name"].nunique())

df = df.dropna(subset=["popularity", "followers"])
df = df[df["followers"] > 0]

top_pop = df.nlargest(10, "popularity")
top_followers = df.nlargest(10, "followers")

sns.barplot(data=top_pop, x="popularity", y="name")
plt.title("Top 10 Artists by Popularity")
plt.show()

sns.barplot(data=top_followers, x="followers", y="name")
plt.title("Top 10 Artists by Followers")
plt.show()

df["log_followers"] = np.log(df["followers"])
print("Correlation:", df["popularity"].corr(df["log_followers"]))

X = add_constant(df["log_followers"])
y = df["popularity"]

model = OLS(y, X).fit()
print(model.summary())

df["genre_count"] = df["genres"].apply(lambda x: len(str(x).split(",")))

sns.boxplot(data=df, x="genre_count", y="popularity")
plt.title("Genre count vs Popularity")
plt.show()
