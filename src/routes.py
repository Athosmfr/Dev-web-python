# Aqui vão as rotas e os links
from src import app
from flask import render_template, url_for, redirect
from flask_login import login_required, login_user, current_user
from src.models import load_user, Posts
from src.forms import FormLogin, FormCreateNewAccount, FormCreateNewPost
from src import bcrypt
from src.models import User
from src import database

import os
from werkzeug.utils import secure_filename


# @app.route('/home')
@app.route('/', methods=['POST', 'GET'])
def homepage():
    _formLogin = FormLogin()

    if _formLogin.validate_on_submit():
        email = _formLogin.email.data
        password = _formLogin.password.data
        user = User.query.filter_by(email=email).first()

        if user:
            if bcrypt.check_password_hash(user.password, password):
                login_user(user, remember=True)

                return redirect(url_for('profile', user_id=user.id))
        else:
            print('Falha na autenticação. Verifique seu e-mail e senha.')

    return render_template('home.html', textinho='TOP', form=_formLogin)


@app.route('/login', methods=['POST', 'GET'])
def createAccount():
    _formCreateNewAccount = FormCreateNewAccount()

    if _formCreateNewAccount.validate_on_submit():
        password = _formCreateNewAccount.password.data

        password_cr = bcrypt.generate_password_hash(password).decode('utf-8')
        # print(password)
        # print(password_cr)

        newUser = User(
            username=_formCreateNewAccount.username.data,
            email=_formCreateNewAccount.email.data,
            password=password_cr
        )

        database.session.add(newUser)
        database.session.commit()

        login_user(newUser, remember=True)
        return redirect(url_for('profile', user_id=newUser.id))

    return render_template('login.html', form=_formCreateNewAccount)


@app.route('/main')
def main():
    return render_template('main.html')


@app.route('/teste')
def teste():
    return render_template('teste.html')


@app.route('/profile/<user_id>', methods = ['POST', 'GET'])  # /<batata>')
@login_required
def profile(user_id):  # , batata):
    if int(user_id) == int(current_user.id):
        _formCreateNewPost = FormCreateNewPost()

        if _formCreateNewPost.validate_on_submit():
            photo_file = _formCreateNewPost.photo.data
            photo_name = secure_filename(photo_file.filename)

            photo_path = f'{os.path.abspath(os.path.dirname(__file__))}/{app.config["UPLOAD_FOLDER"]}/{photo_name}'
            photo_file.save(photo_path)

            _postText = _formCreateNewPost.text.data
            newPost = Posts(post_text=_postText, post_img=photo_name, user_id=int(current_user.id))
            database.session.add(newPost)
            database.session.commit()

        return render_template('profile.html', user=current_user, form=_formCreateNewPost)
    else:
        _user = User.query.get(int(user_id))
        return render_template('profile.html', user=user_id, form=None)  # , mesa=batata)

