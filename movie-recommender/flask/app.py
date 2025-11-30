import requests,pandas as pd,os,json
from top_picks import create_recommendation
from flask import Flask, render_template, request, url_for, redirect, jsonify

movies_5000 = pd.read_csv("tmdb_5000_movies.csv")
dt=pd.read_csv("poster_paths_id.csv")
movies_dt=pd.read_csv("movie.csv")
poster_dt=pd.read_csv("poster_paths_id.csv")

app = Flask(__name__)


tmdb_api_key = 'f8ecd9361b4bb5f50fedd44ab74d585a'


# @app.route("/", methods=["GET","POST"])
# def index():
#     url = 'https://api.themoviedb.org/3/movie/19995?api_key=f8ecd9361b4bb5f50fedd44ab74d585a'
#     response = requests.get(url)
#     poster_url = None
#     if response.status_code == 200:
#         data = response.json()
#         poster_path = data["belongs_to_collection"].get("poster_path")
#         if poster_path:
#             poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
#     return render_template("index.html", poster_url=poster_url)




@app.route("/")
def index():
    trending_name = sorted(list(movies_5000[movies_5000.popularity >= 140].original_title))[:22]
    trending=[]
    for movie_name in trending_name:
        try:
            m_id=movies_dt[movies_dt.title_x == movie_name].iloc[0]['movie_id']
            poster_path = poster_dt[poster_dt.id == m_id].iloc[0]['poster_path']  # Your column name
            poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if pd.notna(poster_path) else None
        except:
            poster_url = None
            
        trending.append({'name': movie_name, 'poster_url': poster_url})

    if os.path.exists("watchlist.json"):
        with open("watchlist.json", "r") as f:
            watchlist_ids = json.load(f)
    else:
        watchlist_ids = []
    
    # Convert to movie names
    watchlist_movies = []
    for movie_id in watchlist_ids:
        try:
            movie_name = movies_dt[movies_dt.movie_id == movie_id].title_x.iloc[0]
            watchlist_poster_path = poster_dt[poster_dt.id == movie_id].iloc[0]['poster_path']  # Your column name
            watchlist_poster_url = f"https://image.tmdb.org/t/p/w500{watchlist_poster_path}" if pd.notna(poster_path) else None
            watchlist_movies.append({"movie_name":movie_name,"watchlist_poster_url":watchlist_poster_url})
        except:
            pass

    recommended_watchlist_movies=[]
    recommended_watchlist_names=create_recommendation(watchlist_ids)
    for rec_movie_name in recommended_watchlist_names:
        try:
            id = movies_dt[movies_dt.title_x == rec_movie_name].movie_id.iloc[0]
            recommended_poster_path = poster_dt[poster_dt.id == id].iloc[0]['poster_path']  # Your column name
            recommended_poster_url = f"https://image.tmdb.org/t/p/w500{recommended_poster_path}" if pd.notna(poster_path) else None
            recommended_watchlist_movies.append({"rec_movie_name":rec_movie_name,"recommended_poster_url":recommended_poster_url})
        except:
            pass

    return render_template('index.html',trending=trending ,watchlist=watchlist_movies,recommended_watchlist_movies=recommended_watchlist_movies)



@app.route('/toggle_watchlist', methods=['POST'])
def toggle_watchlist():
    movie_name = request.form.get('movie_name')  # Use .get() to avoid KeyError
    if not movie_name:
        return jsonify({'error': 'No movie name'}), 400
        
    try:
        id = int(movies_dt[movies_dt.title_x == movie_name].movie_id.iloc[0])
    except:
        return jsonify({'error': 'Movie not found'}), 400
        
    if not os.path.exists("watchlist.json"):
        watch_list = []
    else:
        with open("watchlist.json", "r") as f:
            watch_list = json.load(f)
    
    if id not in watch_list:
        watch_list.append(id)
        in_watchlist = True
    else:
        watch_list.remove(id)
        in_watchlist = False
    
    with open("watchlist.json", "w") as f:
        json.dump(watch_list, f)
    
    return jsonify({'in_watchlist': in_watchlist})



if __name__ == "__main__":
    app.run(debug=True)