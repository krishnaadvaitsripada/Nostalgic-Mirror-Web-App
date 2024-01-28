from flask import Flask, request, redirect, session, url_for
import requests
import json

app = Flask(__name__)
app.secret_key = 'toloteelayalayolokhakayahanrakhdemaharaj1286@65319'  # Set a secret key for session management

# Load client configuration from config.json
with open('config/config.json') as config_file:
    config = json.load(config_file)['web']

# Google API endpoints
AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
PHOTOS_API_URL = "https://photoslibrary.googleapis.com/v1/mediaItems"

# Flask routes
@app.route('/')
def index():
    if 'access_token' in session:
        return "You are already authenticated. <a href='/photos'>Fetch Photos</a>"
    else:
        return redirect(url_for('login'))

@app.route('/login')
def login():
    params = {
        'client_id': config['client_id'],
        'redirect_uri': config['redirect_uris'][0],
        'access_type': 'offline',
        'response_type': 'code',
        'scope': 'https://www.googleapis.com/auth/photoslibrary.readonly',
        'state': 'new_access_token',
        'include_granted_scopes': 'true',
        'prompt': 'consent'
    }
    auth_url = f"{AUTH_URL}?{'&'.join(f'{key}={value}' for key, value in params.items())}"
    return redirect(auth_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    if code:
        # Exchange code for refresh token
        token_data = {
            'client_id': config['client_id'],
            'client_secret': config['client_secret'],
            'code': code,
            'redirect_uri': config['redirect_uris'][0],
            'grant_type': 'authorization_code'
        }
        response = requests.post(TOKEN_URL, data=token_data)
        if response.status_code == 200:
            access_token = response.json().get('access_token')
            refresh_token = response.json().get('refresh_token')
            session['access_token'] = access_token
            session['refresh_token'] = refresh_token
            return "Authentication successful. <a href='/photos'>Fetch Photos</a>"
    return "Authentication failed."

@app.route('/photos')
def fetch_photos():
    if 'access_token' in session:
        access_token = session['access_token']
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }
        params = {'pageSize': 2}
        response = requests.get(PHOTOS_API_URL, headers=headers, params=params)
        if response.status_code == 200:
            media_items = response.json().get('mediaItems', [])
            photo_urls = [item.get('baseUrl', '') for item in media_items]
            return f"Photos: {', '.join(photo_urls)}"
    return "Authentication required. <a href='/login'>Login</a>"

if __name__ == '__main__':
    app.run(debug=True)
