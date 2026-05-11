import requests
from flask import Flask, render_template, request

app = Flask(__name__)
API_KEY = "9aef93600dfd4586b1e8b3014a8a089a"

@app.route('/', methods=['GET', 'POST'])
def home():
    movies = []
    if request.method == 'POST':
        query = request.form.get('search_query')
        if query:
            url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={query}&language=en-US"
            response = requests.get(url)
            movies = response.json().get('results', [])
    else:
        # Trending movies on home page
        url = f"https://api.themoviedb.org/3/trending/movie/day?api_key={API_KEY}"
        response = requests.get(url)
        movies = response.json().get('results', [])
        
    return render_template('index.html', movies=movies)

@app.route('/movie/<int:movie_id>')
def movie_details(movie_id):
    
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&append_to_response=videos,credits"
    response = requests.get(url)
    movie = response.json()
    
    # Extracting Trailer Key
    trailer_key = ""
    for video in movie.get('videos', {}).get('results', []):
        if video['type'] == 'Trailer' and video['site'] == 'YouTube':
            trailer_key = video['key']
            break

    return render_template('details.html', movie=movie, trailer=trailer_key)

if __name__ == '__main__':
    app.run(debug=True)