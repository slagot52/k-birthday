from flask import Flask, redirect, url_for, session, render_template
from authlib.integrations.flask_client import OAuth
import os

# Initialize the Flask application
app = Flask(__name__)
app.secret_key = os.urandom(24)

# OAuth configuration
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id='YOUR_GOOGLE_CLIENT_ID',
    client_secret='YOUR_GOOGLE_CLIENT_SECRET',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    userinfo_endpoint='https://www.googleapis.com/oauth2/v1/userinfo',
    client_kwargs={'scope': 'openid profile email'},
)

@app.route('/')
def homepage():
    email = dict(session).get('email', None)
    return render_template('homepage.html', email=email)

@app.route('/login')
def login():
    return google.authorize_redirect(url_for('authorize', _external=True))

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('homepage'))

@app.route('/authorize')
def authorize():
    response = google.authorize_access_token()
    user_info = google.get('userinfo').json()
    session['email'] = user_info['email']
    return redirect(url_for('homepage'))

@app.route('/reports')
def reports():
    email = dict(session).get('email', None)
    return render_template('layout.html', email=email)

if __name__ == '__main__':
    app.run(ssl_context='adhoc')