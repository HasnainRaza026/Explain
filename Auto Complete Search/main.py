import requests
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

# Replace with your own TMDb API key
TMDB_API_KEY = 'your_api_key'

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('search_query')
def handle_search(query):
    print(f"Received query: {query}")

    # TMDb API endpoint
    url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={query}"
    response = requests.get(url)
    
    # Handle API response
    if response.status_code == 200:
        data = response.json()
        # Extract relevant fields: title, year, and optionally poster
        results = [
            {
                "title": movie["title"],
                "year": movie.get("release_date", "N/A")[:4],  # Extract year from release_date
                "poster": f"https://image.tmdb.org/t/p/w200{movie['poster_path']}" if movie.get("poster_path") else None
            }
            for movie in data.get("results", [])
        ]
    else:
        print(f"Error fetching data from TMDb: {response.status_code}")
        results = []

    emit('search_results', results)

if __name__ == '__main__':
    socketio.run(app, debug=True)
