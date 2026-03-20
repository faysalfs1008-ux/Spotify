import streamlit as st
import matplotlib.pyplot as plt
from data_loader_marta import (
    get_artists_data,
    get_features_data,
    get_available_features,
    get_available_genres
)

st.set_page_config(page_title="Spotify Dashboard", layout="wide")

artists_df = get_artists_data()
features_df = get_features_data()

available_features = get_available_features(features_df)
available_genres = get_available_genres(features_df)

st.sidebar.title("Spotify Dashboard")

page = st.sidebar.radio(
    "Go to",
    ["Home", "Feature Analysis", "Genre Analysis", "Artist Search"]
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
    st.write("This dashboard explores artist and track statistics from the Spotify dataset.")

    col1, col2, col3 = st.columns(3)
    col1.metric("Number of artists", artists_df["artist_name"].nunique())
    col2.metric("Average popularity", round(artists_df["popularity"].mean(), 2))
    col3.metric("Average followers", round(artists_df["followers"].mean(), 2))

    st.subheader("Top Artists by Popularity")
    top_pop = artists_df.sort_values("popularity", ascending=False)

    fig, ax = plt.subplots()
    ax.bar(top_pop["artist_name"], top_pop["popularity"])
    ax.set_xlabel("Artist")
    ax.set_ylabel("Popularity")
    plt.xticks(rotation=45)
    st.pyplot(fig)

    st.subheader("Dataset Preview")
    st.dataframe(artists_df)

elif page == "Feature Analysis":
    st.title("Feature Analysis")
    st.write(f"Distribution of **{selected_feature}** for the selected year range.")

    fig, ax = plt.subplots()
    ax.hist(filtered_features[selected_feature], bins=10)
    ax.set_xlabel(selected_feature)
    ax.set_ylabel("Count")
    st.pyplot(fig)

    st.subheader("Filtered Tracks")
    st.dataframe(filtered_features[["track_name", "artist_name", selected_feature, "genre", "year"]])

elif page == "Genre Analysis":
    st.title("Genre Analysis")

    genre_data = filtered_features[filtered_features["genre"] == selected_genre]

    st.write(f"Showing results for genre: **{selected_genre}**")

    if genre_data.empty:
        st.warning("No data available for this genre in the selected year range.")
    else:
        avg_value = genre_data[selected_feature].mean()
        st.metric(f"Average {selected_feature}", round(avg_value, 3))

        fig, ax = plt.subplots()
        ax.bar(genre_data["track_name"], genre_data[selected_feature])
        ax.set_xlabel("Track")
        ax.set_ylabel(selected_feature)
        plt.xticks(rotation=45)
        st.pyplot(fig)

        st.dataframe(genre_data)

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