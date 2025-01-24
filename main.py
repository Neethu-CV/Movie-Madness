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
  "private_key_id": "27b7fde643b957f8617436c35fce492743406084",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCt/W05Czrqetij\nesTNpadstKp+B9sbTo7Hn0KOs+6XNoLXaJgX5ZHQieqSkmo4RciZIX+6sY6QuJ7u\ngRXKJoCw8DGhVdgHNon04zUyq/YWAT+VLidlb29f7x2vCO0/0K4FCY4M/RGlbjBA\nuhNT9/UL8TjR6cOlpaHYvv3qAzAqS/9aTm3qmej7wNaLLcZsSdq5yL/VwqaAiKtk\niaii07/miVKAcdWrhfWq0xmHBukGteelPvBnjEMWZ+BLAkIWOB0kJZOuftbVJxsL\n0AG6l3qiqya3RvBjJVHGvuuYrLN4O2vilLf1lfK3x2JhhIorTsLB/RFyBD3GZAQG\nSbN5PU7LAgMBAAECggEAMLWn29X4hwegWdg3e6k6P5Uuu/zgCvuJvnooLIJUM/I3\nXC30kpAbK+pIiQNDiICE4dX+h9pIotyE5hmua3svARolktjRE2fh5HStgoOg79Um\no1GaBuxVHmL3iPazUO/PoCpmId3BkHJSQPS3D4V2DYNZWG8c7mV584+4z0hYNia8\nxUGAFy0m7qFQAJ6g8l+JFmeYhdQr/n2V4SSjNuiNKm+uZqp+T+yawKLQXJpDerPg\nLc9UymjU7eZ8lAkjtSRy+uFZ5n78/T1H3Mevkl2eNFmgvmp6x2mfjjxdNGyekO3w\nJ6Y0EnBGBVrL7NjSyc7ZN2BNVH++TCpU7vZktQKY8QKBgQDqMjnqSY7kMBayCDiw\nVWkggC59GCOOD/bIbiyX4JLl1xBd08Zk97PdScrudt0R7znFn7x6K2nEH+JF6TsP\nuV4VZ4Ry8E3UFMmFh7X9npn1LoE47EYWFi88QuEdWe8GrhMMOe7HyDSdLYqMMQxS\nNjSMjvox8U+5wKcAlI+b4MXQ0QKBgQC+MEJ751kcgScoibOlfyz5Ll4zn7QuQn1N\nCu/RDKc5DTiip57HQM0ubZwG0l8Y2+a4bHl9H88KCOm1RphMO/2SyxnSuklEmxDZ\nUa6r/UcGImjMk92R+j493mTHh5y2Iy1G5Ci6qoS/Proy/N5Upk8HqAiXQfVH3a9T\nBvgVFBPs2wKBgBw+sn1vIayjoBkYpL2fj248B19O6frYMgs6PmaSzySpK3Alemfy\n995YaAEalM706yLKgRC666absc58soLS+GXcdjzmfnx1hVh1ZZ2Q40COu0cCN/Gx\n+0BpUH0Zu5oypFl1Izc1DiNmuq7tu26u2ueY1tPvJo5gjcOkJy3FjhYBAoGAEr/1\nPfvf2CSPdLqmoFE6YNKGbPZ4r/rUGY1TeTuTHNfF1ptJ1wD3eXVK5Y1F3NCJHXNs\nQr6pDac1Sy7LgvCDHj6xrAm7gWz8K0CXRNNydhNcW5bUSDjwe+755oXjGD29j/ic\nX1LCRYxslOxDCvteXTXeqvLQuKYNS9UrDgDtufMCgYEAtrDsVn912u4qzhG865dp\nA+praF4pVr9XnSsMeFoXnhHKPI7UMso1XBTZZwoOUFi+pM5VmY2l9W9SY94hnS6W\n3TB5FH4Hwnglu0QpiB93l/Iw3gCyvv2xKo4ExRFPbHufRbab58vbMZl2uwXwKGbG\nJQy4xe2PmwFcJeAo4okqyYU=\n-----END PRIVATE KEY-----\n",
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

