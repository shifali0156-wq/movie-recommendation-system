import requests
from flask import Flask, render_template, request, url_for

app = Flask(__name__)


tmdb_api_key = 'f8ecd9361b4bb5f50fedd44ab74d585a'

@app.route("/", methods=["GET","POST"])
def index():
    url = 'https://api.themoviedb.org/3/movie/19995?api_key=f8ecd9361b4bb5f50fedd44ab74d585a'
    response = requests.get(url)
    poster_url = None
    if response.status_code == 200:
        data = response.json()
        poster_path = data["belongs_to_collection"].get("poster_path")
        if poster_path:
            poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
    return render_template("index.html", poster_url=poster_url)


if __name__ == "__main__":
    app.run(debug=True)

