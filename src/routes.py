# Aqui vão as rotas e os links!
from src import app
from flask import render_template
from flask import url_for

@app.route('/')
# @app.route('/home')
def homepage():
    return render_template('home.html', texto='EAShnou')

@app.route('/profile/<user_id>') # /<batata>
def profile(user_id):
    return render_template('profile.html', user=user_id) # mesa=batata

@app.route('/main')
def main():
    return render_template('main.html')


@app.route('/teste')
def teste():
    return render_template('teste.html')