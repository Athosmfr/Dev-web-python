from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__) # vai pegar nome do projeto
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comunidade.db'

database = SQLAlchemy(app)

from src import routes
