from movie_recommender_py import recommend
from top_picks import create_recommendation
import streamlit as st
import pandas as pd
import ast,requests
import json
import os

movies_5000 = pd.read_csv("tmdb_5000_movies.csv")
movie_df=pd.read_csv("movie_redefined.csv")
df=pd.read_csv("movie.csv")
trending = sorted(list(movies_5000[movies_5000.popularity >= 150].original_title))

def images(id):
    url = f"https://api.themoviedb.org/3/movie/{id}?api_key=f8ecd9361b4bb5f50fedd44ab74d585a"
    # try:
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    print(data)  # <-- Add
    poster_path = data.get("poster_path")
    if poster_path:
        return f"https://image.tmdb.org/t/p/w500/{poster_path}"
        '''else:
            return "images.png"
    except Exception as e:
        print(f"Error fetching from TMDB: {e}")  # <-- Add
        return "images.png"
'''

'''
def images(id):
    url = f"https://api.themoviedb.org/3/movie/{id}?api_key=f8ecd9361b4bb5f50fedd44ab74d585a"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get("poster_path")
        if poster_path:
            # Return TMDB poster image URL
            return f"https://image.tmdb.org/t/p/w500/{poster_path}"
        else:
            return "images.png"   # Local fallback path
    except Exception as e:
        return "images.png"'''



'''def images(id):
    response=requests.get(f"https://api.themoviedb.org/3/movie/{id}?api_key=f8ecd9361b4bb5f50fedd44ab74d585a")
    data=response.json()
    return "https://image.tmdb.org/t/p/w500"+data['poster_path']'''

grid_cols = 4  # Number of movies per row

def watchlist(id):
    if isinstance(id, pd.Series):
        id = int(id.iloc[0])
    elif isinstance(id, (list, tuple)):
        id = int(id[0])
    else:
        id = int(id)
    
    if not os.path.exists("watchlist.json"):
        watch_list=[]
    else:
        f=open("watchlist.json","r")
        try:
            watch_list=json.load(f)
        except json.JSONDecodeError:
            watch_list = []
        f.close()
    if id not in watch_list:
        watch_list.append(id)
        t=open("watchlist.json","w")
        json.dump(watch_list,t)
    return watch_list

def remove_from_watchlist(id):
    if not os.path.exists("watchlist.json"):
        return
    with open("watchlist.json", "r") as f:
        try:
            watch_list = json.load(f)
        except json.JSONDecodeError:
            watch_list = []
    if id in watch_list:
        watch_list.remove(id)
        with open("watchlist.json", "w") as t:
            json.dump(watch_list, t)


# Session state for rows shown
if 'shown_rows' not in st.session_state:
    st.session_state.shown_rows = 1
if 'page' not in st.session_state:
    st.session_state.page = "home"
if 'selected_movie' not in st.session_state:
    st.session_state.selected_movie = None

f=open("watchlist.json","r")
watch_list_id=json.load(f)

if st.session_state.page == "home":
    movie=st.selectbox("SELECT THE MOVIE",movie_df.title_x)    
    recommendations=recommend(movie)
    if st.button("Recommend"):
        st.write(recommendations)
    st.header("TRENDING NOW")
    # Split trending list into rows
    rows = [trending[i:i+grid_cols] for i in range(0, len(trending), grid_cols)]
    # Only show up to `shown_rows` rows
    for i in range(st.session_state.shown_rows):
        if i >= len(rows): break
        cols = st.columns(grid_cols)
        for idx, movie in enumerate(rows[i]):
            with cols[idx]:
                id=int(movie_df[movie_df.title_x==movie].movie_id.iloc[0])
                if id not in watch_list_id:
                    if st.button("+WATCHLIST", key=f"watchlist_{movie}_{i}"):
                        watchlist(id)
                else:
                    if st.button("-REMOVE", key=f"remove_{id}_{i}_{idx}"):
                        remove_from_watchlist(id)
                        st.rerun()                 
                st.image(images(id), use_container_width=True)
                if st.button(movie, key=f"trend_{movie}_{i}",type="tertiary"):
                    st.session_state.page = "details"
                    st.session_state.selected_movie = movie
                    # See more button IF not all rows shown
    if st.session_state.shown_rows < len(rows):
        if st.button("See more",key="watchlist-see_more"):
            st.session_state.shown_rows += 1
            st.rerun()
    st.header("YOUR WATCHLIST")
    
    rows = [watch_list_id[i:i+grid_cols] for i in range(0, len(watch_list_id), grid_cols)]
    # Only show up to `shown_rows` rows
    for i in range(st.session_state.shown_rows):
        if i >= len(rows): break
        cols = st.columns(grid_cols)
        for idx, id in enumerate(rows[i]):
            with cols[idx]:               
                st.image(images(id), use_container_width=True)
                movie_title = movie_df[movie_df.movie_id==id].iloc[0].title_x 
                if st.button(str(movie_title), key=f"watch_list_id_{movie_title}_{i}_{id}",type="tertiary"):
                    st.session_state.page = "details"
                    st.session_state.selected_movie = str(movie_title)
                    # See more button IF not all rows shown
    if st.session_state.shown_rows < len(rows):
        if st.button("See more",key="See_more"):
            st.session_state.shown_rows += 1
            st.rerun()

    st.header("Top Picks Just For You")
    top_picks_list=create_recommendation(watch_list_id)
    
    rows = [top_picks_list[i:i+grid_cols] for i in range(0, len(top_picks_list), grid_cols)]
    # Only show up to `shown_rows` rows
    for i in range(st.session_state.shown_rows):
        if i >= len(rows): break
        cols = st.columns(grid_cols)
        for idx, movie in enumerate(rows[i]):
            with cols[idx]:
                id=int(movie_df[movie_df.title_x==movie].movie_id.iloc[0])
                if id not in watch_list_id:
                    if st.button("+WATCHLIST", key=f"tpfu_{movie}_{i}_{idx}"):
                        watchlist(id)
                else:
                    if st.button("-REMOVE", key=f"remove_{id}_{i}_{idx}"):
                        remove_from_watchlist(id)
                        st.rerun()                
                st.image(images(id), use_container_width=True)
                if st.button(movie, key=f"tpgu_{movie}_{i}_{idx}",type="tertiary"):
                    st.session_state.page = "details"
                    st.session_state.selected_movie = movie
                    # See more button IF not all rows shown
                
    if st.session_state.shown_rows < len(rows):
        if st.button("See more"):
            st.session_state.shown_rows += 1
            st.rerun()
        
    
    

elif st.session_state.page == "details":
    movie_name = st.session_state.selected_movie
    st.header(movie_name)
    st.image(images(id), use_container_width=True)
    movie_row = movie_df[movie_df.title_x == movie_name]
    if not movie_row.empty:
        movie_row.genres=movie_row.genres.apply(ast.literal_eval)
        genre=movie_row.iloc[0]['genres']
        for i in genre:
            st.button(i)
        # st.write(f"Popularity: {movie_row_500.iloc[0]['popularity']}")
    if st.button("Back to Trending"):
        st.session_state.page = "home"
        st.session_state.selected_movie = None
        # Optional: Reset rows to first row on return
        st.session_state.shown_rows = 1

st.write("hi")