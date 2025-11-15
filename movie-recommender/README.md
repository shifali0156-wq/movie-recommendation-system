<h1>Movie Recommender</h1>
<br>
<p>A modern Streamlit-based web app for movie recommendations and personal watchlist management.</p>
<p>Choose your favourite movies, get smart recommendations, build your watchlist, and explore trending picks in a clean, interactive gallery/grid.</p>

<h3>Features-</h3>
<p>Trending Now: Browse popular movies in a responsive grid—see more rows with a click.</p>
<p>Smart Recommendations: Select any movie and instantly view recommended titles using the built-in recommender.</p>
<p>Watchlist: Add any movie to your personal watchlist to revisit later—see all your picks in an organized gallery.</p>
<p>Movie Details: Click any movie name to view details, including genres and quick back navigation.</p>
<p>Top Picks: Discover top suggestions curated just for you.</p>

<h3>Prerequisites</h3>
<p>Python 3.8+</p>
<p>Pip</p>
<p>Streamlit</p>

<h3>Installation</h3>
<h5>Clone the repository</h5>
<p>git clone https://github.com/shifali0156-wq/BEGINNERS-PROJECT.git</p>
<p>cd movie-recommender</p>

<h5>Create and activate a virtual environment</h5>
<p>python -m venv venv</p>
<p>venv\Scripts\activate     # On Windows</p>

<h5>Install required packages</h5>
<p>pip install -r requirements.txt</p>

<h5>Prepare dataset files</h5>
<p>movie.csv</p>
<p>tmdb_5000_movies.csv</p>
<p>movie_redefined.csv</p>

<h3>Interact with UI</h3>
<p>Select movies from drop-downs or the trending grid.</p>
<p>Click to add/remove movies to your watchlist.</p>
<p>View recommended movies and details pages.</p>

<h3>Code Structure</h3>
<p>frontend3.py - Main Streamlit app and UI logic</p>
<p>movie_recommender_py.py - Recommender model functions</p>
<p>movie.csv / tmdb_5000_movies.csv / movie_redefined.csv - Movie datasets</p>
<p>watchlist.json - User’s persistent watchlist</p>
<p>images.png - Poster images in grid/gallery</p>

<h3>Customization</h3>
<p>To add movie-specific images: update code to map each movie to its unique poster file.</p>
<p>To change grid size: update grid_cols variable in the app.</p>

<h3>Troubleshooting</h3>
<p>Virtualenv issues: Be sure to activate your environment and install packages within it.</p>
<p>CSV/file errors: Make sure all dataset files exist and have the correct format.</p>
<p>Streamlit/settings: Use latest Streamlit for full compatibility with modern UI features.</p>

<h4>I'm stil working on the project, so this is a temporary readme.</h4>
