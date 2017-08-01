# flask imports
from flask import Flask, render_template, request, redirect, url_for

# SQLAlchemy
from model import Base, Recipe
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# setup
app = Flask(__name__)
engine = create_engine('sqlite:///project.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()



@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/post/<int:post_id>')
def post_recipe(post_id):
	recipe = session.query(Recipe).filter_by(id = post_id).first()
    return render_template('post.html', recipe = recipe)

@app.route('/countries/<string:country>')
def country_page(country):
	recipes = session.query(Recipe).filter_by(country = country).all()
	return render_template('country.html', recipes = recipes, country = country)

Base.metadata.create_all(engine)