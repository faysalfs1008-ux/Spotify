import streamlit as st
import matplotlib.pyplot as plt
from data_loader import (
    get_artists_data,
    get_features_data,
    get_available_features,
    get_available_genres,
    load_explicit_popularity,
    load_collaboration_popularity,
    load_album_artist_popularity,
    load_top_danceability_artists
)

st.set_page_config(page_title="Spotify Dashboard", layout="wide")

artists_df = get_artists_data()
features_df = get_features_data()

available_features = get_available_features(features_df)
available_genres = get_available_genres(features_df)

st.sidebar.title("Spotify Dashboard")

page = st.sidebar.radio(
    "Go to",
    ["Home", "Feature Analysis", "Genre Analysis", "Artist Search", "Insights"]
)

selected_feature = st.sidebar.selectbox(
    "Select a feature",
    available_features
)

selected_genre = st.sidebar.selectbox(
    "Select a genre",
    available_genres
)

artist_search = st.sidebar.text_input("Search for an artist")

year_min = int(features_df["year"].min())
year_max = int(features_df["year"].max())

selected_years = st.sidebar.slider(
    "Select year range",
    year_min,
    year_max,
    (year_min, year_max)
)

filtered_features = features_df[
    (features_df["year"] >= selected_years[0]) &
    (features_df["year"] <= selected_years[1])
]

if page == "Home":
    st.title("Spotify Data Dashboard")
    st.write("This dashboard provides an overview of Spotify artist and track statistics. "
             "Use the sidebar to explore artist information, features, genres, and year-based trends.")
    
    st.subheader("General Statistics")
    col1, col2, col3 = st.columns(3)

    col1.metric("Number of artists", artists_df["artist_name"].nunique())
    col2.metric("Average popularity", round(artists_df["popularity"].mean(), 2))
    col3.metric("Average followers", f"{int(artists_df['followers'].mean()):,}")

    st.subheader("Top Artists by Popularity")
    top_pop = artists_df.sort_values("popularity", ascending=False).head(10)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(top_pop["artist_name"], top_pop["popularity"])
    ax.set_xlabel("Artist")
    ax.set_ylabel("Popularity")
    ax.set_title("Top 10 Artists by Popularity")
    plt.xticks(rotation=45)
    st.pyplot(fig)

    st.subheader("Top Artists Overview")
    st.dataframe(
        top_pop[["artist_name", "popularity", "followers"]]
        .reset_index(drop=True)
    )

elif page == "Feature Analysis":
    st.title("Feature Analysis")
    st.write(f"Distribution of **{selected_feature}** for the selected year range.")

    fig, ax = plt.subplots()
    ax.hist(filtered_features[selected_feature], bins=10)
    ax.set_xlabel(selected_feature)
    ax.set_ylabel("Count")
    st.pyplot(fig)

    st.subheader("Filtered Tracks")
    st.dataframe(filtered_features[["artist_name", selected_feature, "popularity", "explicit", "year"]])

elif page == "Genre Analysis":
    st.title("Genre Analysis")

    genre_data = filtered_features[filtered_features["genre"] == selected_genre]

    st.write(f"Showing results for genre: **{selected_genre}**")

    if genre_data.empty:
        st.warning("No data available for this genre in the selected year range.")
    else:
        avg_value = genre_data[selected_feature].mean()
        avg_popularity = genre_data["popularity"].mean()

        col1, col2 = st.columns(2)
        col1.metric(f"Average {selected_feature}", round(avg_value, 3))
        col2.metric("Average popularity", round (avg_popularity, 2))

        st.subheader(f"Top Artists in {selected_genre}")

        top_genre_data = (
            genre_data.groupby("artist_name")[[selected_feature, "popularity"]]
            .mean()
            .sort_values(selected_feature, ascending=False)
            .head(10)
            .reset_index()
        )

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(top_genre_data["artist_name"], top_genre_data[selected_feature])
        ax.set_xlabel("Artist")
        ax.set_ylabel(selected_feature)
        ax.set_title(f"Top Artists in {selected_genre} by {selected_feature}")
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(fig)

        st.subheader("Tracks in Selected Genre")
        st.dataframe(
            genre_data[["artist_name", "genre", selected_feature, "popularity", "explicit", "year"]]
            .reset_index(drop=True)
            )

elif page == "Artist Search":
    st.title("Artist Search")

    if artist_search:
        result = artists_df[
            artists_df["artist_name"].str.contains(artist_search, case=False, na=False)
        ]

        if result.empty:
            st.warning("No artist found.")
        else:
            st.success(f"Found {len(result)} matching artist(s).")
            st.dataframe(result)
    else:
        st.info("Enter an artist name in the sidebar to search.")

elif page == "Insights":
    st.title("Analysis Insights")

    explicit_df = load_explicit_popularity()
    collaboration_df =load_collaboration_popularity()
    album_artist_df = load_album_artist_popularity()
    danceability_df = load_top_danceability_artists()

    # Explicit vs Non-Explicit
    st.subheader("Explicit vs Non-Explcit Tracks")

    fig, ax = plt.subplots()
    ax.bar(explicit_df["explicit_label"], explicit_df["average_popularity"])
    ax.set_xlabel("Track Type")
    ax.set_ylabel("Average Popularity")
    ax.set_title("Average Popularity of Explicit vs Non-Explicit Tracks")
    plt.tight_layout()
    st.pyplot(fig)

    st.write("Explicit tracks appear to have a higher average popularity than non-explicit tracks.")

    # Collaboration vs Solo
    st.subheader("Collaborration vs Solo Tracks")

    fig, ax = plt.subplots()
    ax.bar(collaboration_df["collaboration_label"], collaboration_df["average_popularity"])
    ax.set_xlabel("Track Type")
    ax.set_ylabel("Average Popularity")
    ax.set_title("Average Popularity of Collaboration vs Solo Tracks")
    plt.tight_layout()
    st.pyplot(fig)

    st.write("Collaborative tracks appear to perform better on average than solo tracks in this dataset.")

    # Album vs Artist popularity
    st.subheader("Album vs Artist Popularity")

    fig, ax = plt.subplots()
    ax.scatter(
        album_artist_df["artist_popularity"], 
        album_artist_df["album_popularity"], 
        alpha=0.5
    )
    ax.set_xlabel("Artist Popularity")
    ax.set_ylabel("Album Popularity")
    ax.set_title("Relationship between Artist and Album Popularity")
    plt.tight_layout()
    st.pyplot(fig)

    st.write("This scatter plot suggests a positive relationship between artist popularity and album popularity.")

    # Top danceability artists
    st.subheader("Top Danceability Artists")

    fig, ax = plt.subplots()
    ax.barh(danceability_df["artist_name"], danceability_df["number_of_top_tracks"])
    ax.set_xlabel("Number of Top Tracks")
    ax.set_ylabel("Artist")
    ax.set_title("Artist Appearing Most in Top 10% Danceability Tracks")
    plt.tight_layout()
    st.pyplot(fig)

    st.write("These artists appear most often among the top 10% most danceable tracks.")

    # Feature over time
    st.subheader("Feature Trends Over Time")

    trend_data = filtered_features.groupby("year").agg(
        avg_value=(selected_feature, "mean"),
        count=("id", "count")
    ).reset_index()

    trend_data = trend_data[trend_data["count"] >= 20]
    
    fig, ax = plt.subplots()
    ax.plot(trend_data["year"], trend_data["avg_value"])
    ax.set_xlabel("Year")
    ax.set_ylabel(f"Average {selected_feature}")
    ax.set_title(f"Average {selected_feature.capitalize()} Over Time")
    ax.grid(alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig)

    st.write(f"This chart shows how average {selected_feature} changes over time in the selected year range.")
