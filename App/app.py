import streamlit as st
import pickle
import pandas as pd
import requests

# Fetch movie poster from TMDB API
def fetch_poster(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=39a9580e19c35a753219d5d125250451&language=en-US'
    data = requests.get(url).json()
    poster_path = data['poster_path']
    full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
    return full_path


# Recommendation function
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:  # Get top 5 recommendations
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters


# Load movie data
with open('movie_dict.pkl', 'rb') as file:
    movies_dict = pickle.load(file)

movies = pd.DataFrame(movies_dict)

# Load similarity matrix
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit UI
st.title('🎬 Movie Recommender System 🎥')

# Movie select box
selected_movie_name = st.selectbox('Choose a Movie You Like:', movies['title'].values)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie_name)

    # Display 5 recommendations with space between them
    col1, col2, col3, col4, col5 = st.columns([1, 0.2, 1, 0.2, 1])  # Adjusted column widths for spacing

    # Define the poster width
    poster_width = 180

    with col1:
        st.markdown(f"<div style='text-align: center;'><strong>{recommended_movie_names[0]}</strong></div>",
                    unsafe_allow_html=True)
        st.image(recommended_movie_posters[0], width=poster_width)

    with col3:  # Skip col2 to create space
        st.markdown(f"<div style='text-align: center;'><strong>{recommended_movie_names[1]}</strong></div>",
                    unsafe_allow_html=True)
        st.image(recommended_movie_posters[1], width=poster_width)

    with col5:  # Skip col4 to create space
        st.markdown(f"<div style='text-align: center;'><strong>{recommended_movie_names[2]}</strong></div>",
                    unsafe_allow_html=True)
        st.image(recommended_movie_posters[2], width=poster_width)

    # New row for additional movies
    st.markdown("<br>", unsafe_allow_html=True)
    col6, col7, col8, col9, col10 = st.columns([1, 0.2, 1, 0.2, 1])

    with col6:
        st.markdown(f"<div style='text-align: center;'><strong>{recommended_movie_names[3]}</strong></div>",
                    unsafe_allow_html=True)
        st.image(recommended_movie_posters[3], width=poster_width)

    with col8:  # Skip col7 to create space
        st.markdown(f"<div style='text-align: center;'><strong>{recommended_movie_names[4]}</strong></div>",
                    unsafe_allow_html=True)
        st.image(recommended_movie_posters[4], width=poster_width)
