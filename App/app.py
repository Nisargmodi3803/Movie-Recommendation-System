import streamlit as lt
import pickle

movies_list = pickle.loads(open('movies.pkl', 'rb'))
movies_list = movies_list['title'].values

lt.title('Movies Recommender System')
