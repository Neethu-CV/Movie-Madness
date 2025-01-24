import os
import random
from flask import Flask, render_template, request, redirect, send_from_directory, session
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import secrets

import firebase_admin
from firebase_admin import credentials, db

# Initialize Firebase Admin SDK with the provided service account
cred = credentials.Certificate({
  "type": "service_account",
  "project_id": "dum-charades",
  "private_key_id": "f8da4294cc3fc10324b62a33375348971af17476",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQCmCfZiPW4ZwAvF\ng8tle3eIEZjRWBbe2Mc7Mu0lw94bAAKbtjKbm9v+Ke+HYnybTs80N8DxrPMb3mPo\nKyizAymEfXguAjrckNpzGtmhm0YyYMdsqvndpeLW2n8T9nJ6dJu5dFUfTNZkBXfJ\nIhTQPANg0fBOQHqpIxjP3BkiylO/nax+f64Z9OeVopfM/7RCzHSVMllERPFXAraR\nGDvj2DQuD55CJvXU43IczwNh0y14jNLxPAT9ujRNfms/RRA4vl0A+UfoDf0gM9+x\nsOf2ruT9CLjt4HrRCjk9AQx3p5SPiC3beoaKdubE1pPECKa3m7/u/mOGs3CTHbNd\nUebWtwRPAgMBAAECggEAAiO5uY1aGFnZrPtkSRP8t9OmOPheHxQDCTfAR47NE2L+\nJZyE7W1mOdG3hPKXcXbkA6O+SD72yQKmHe1Ecn4VcGAfhtQ/hu0U64vKhyMVlfua\nRkOzwY/sKuGY5pxz4DEVep/NowAd+R766qwWQZKsZnh+FLwO+JP7s13+Mu0RhDQS\nHW1JDIGoFV5q8nYLz0PQXt3pMUWGWK0oyxZ+3JFhKuTXXOSAhzQTRunYjv4FhtK/\nuEpvx/HbD174m5hb1JMCxb1sYM6xGJEVnWhHo/IsjJILfbvsYw8i5gj4zLkpLODn\n7hgtpvxHyxSTcBS1+fdOhKo0lLMIkeLv5tqqVBe+MQKBgQDZCHv3rrH798VnvABM\nARY1bJs53IK5WATuYuYJ/62LnogcNfk6opeiT0RpytQvYH/k8Gx4gg2aj+KJF09z\n37rYURgu89x+hv9uAYNSjlWi4lfb5EbQQB5HULA9ehQv7rM2TBKHAuDBarJwE9ax\nXPfQobX1Qj3ZeSpYmb1nRiHTUQKBgQDD2aAjnJxRnWiv4DHMMqtK7RcHZu9ZvCXO\nKxO+rfvAk8VFMpEIbzINCkiGPPCWd8IxcHg5J/d5Y0OtPQmj8kxRYXVynN5P/Qi8\nt6MI/Hzg39qGtc77W4/0mXJa+ymg8NXvOUg+1ffSygnplv1Yus0DxbZlM8CJB5vP\n1qhMaGU1nwKBgQCEzxRNNLHlpnE+UWU9HU0h1BwJBE9aa+pYllx+sd7ZGWHhIYYp\nw2VXBXqv4laFx198EUPPWoZIltPhYEpWdgo4ZSePU9sR8jpMbtCVrFPrIObywHY0\n6YedzFqMxC+mRUOVbmfIBpLSyR/4RauTTXi4Sry2IJsIgYTQQwQMNnZsgQKBgQC9\nTvrP8W3YJgMvHdKEwuV4AzyjVwg9APS6GEF5qssSFsQ0YvB16qXCnRIFT5pul0wK\nZeCPvuYjW6PrLHjJFEhY0Y+pPaBWSQvM/uSEpyo+Y6LjW5G6vYKkuD4lW2mdu63P\nEtuWgVSPV+PE+sHgpo/M+auYnzGYQtaFS8RaNv69mQKBgQC/FbSdXnTn63bKpS2a\nZ+J9iZaAVT1efEnUuxQKCyWvoIez3Mei4qzyIuSln6/kOgWlxjCX6IKCSeQVaEY9\ncOAcwLXOw1Q+izTxgwTNjF4zKm7GdNUuaijToPBnUWxVilx9ngb+7hOi6DSOdLVB\nwinReUsstCwgxJrJdJjhzuxtww==\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-fbsvc@dum-charades.iam.gserviceaccount.com",
  "client_id": "116453978527181117904",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40dum-charades.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
})

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

