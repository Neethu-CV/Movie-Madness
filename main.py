import os
import random
from flask import Flask, render_template, request, redirect, send_from_directory, session
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import secrets

# Initialize Firebase app
cred = credentials.Certificate('credentials\dum-charades-firebase-adminsdk-fbsvc-b6f7f6eb29.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://dum-charades-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

# Firebase reference
ref = db.reference('movies')

previous_movies=[]
movies=[]
languages=[]
categories=[]

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

# Routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/options', methods=['GET', 'POST'])
def options():
    global movies,languages,categories,previous_movies,movies
    languages = []
    categories = []
    previous_movies = []
    movies = []
    print("line 34")
    return render_template('options.html')

def slecet_random_movies(movies):
    global previous_movies
    while True:
        i = random.randint(0, len(movies) - 1)
        if i not in previous_movies:
            previous_movies.append(i)
            break
    movie=get_movie_by_id(movies[i])
    print("\n\n")
    print(movies[i])
    print(movie)
    return render_template('game.html', movie=movie)

def fetch_movies(languages, categories):
    global movies
    movies=[]
    result_movie=[]
    all_movies = ref.get()
    for language in languages:
        for category in categories:
            for movie in all_movies:
                if movie.startswith(f"{language} {category}"):
                    print(movie)
                    result_movie.append(movie)
    return result_movie

# Fetch the movie data by id from Firebase
def get_movie_by_id(movie_id):
    movie_ref = ref.child(movie_id)
    movie_data = movie_ref.get()
    return movie_data

@app.route('/game', methods=['GET', 'POST'])
def game():
    global movies,languages,categories,previous_movies
    
    if request.method == 'POST':
        if request.form.get('next'):
            current_movie_index += 1
            if current_movie_index >= len(movies):
                return render_template('error.html', message='No more movies left!')
            return slecet_random_movies(movies)
        elif request.form.get('back'):
            languages = []
            categories = []
            previous_movies = []
            movies = []
            return redirect('/options')
    if languages==[]:
        print("line 69")
        languages = request.form.getlist('languages')
        categories = request.form.getlist('categories')
    if not languages or not categories:
        languages=['hindi','kannada','telugu']
        categories=['timeless_classics','new_age_blockbusters']
    if movies==[]:
        movies = fetch_movies(languages, categories)
        random.shuffle(movies) 
        
    return slecet_random_movies(movies)



if __name__ == '__main__':
    app.run(debug=True)

