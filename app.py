# flask imports
from flask import Flask, Response, render_template, request, redirect, url_for

# flask setup
app = Flask(__name__)
app.config["SECRET_KEY"] = "ITSASECRET"

# flask-login imports
from flask_login import login_required, current_user
from login import login_manager, login_handler, logout_handler
login_manager.init_app(app)

# SQLAlchemy
from model import Base, Recipe, User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
engine = create_engine('sqlite:///project.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
def test_homepage():
	return render_template('home.html')

'''
@app.route('/post/<int:post_id>')
def post_recipe(post_id):
    recipe = session.query(Recipe).filter_by(id = post_id).first()
    return render_template('post.html', recipe = recipe)'''


@app.route('/countries/<string:country>')
def country_page(country):
	recipes = session.query(Recipe).filter_by(country = country).all()
	return render_template('country.html', recipes = recipes, country = country)


@app.route('/login', methods=['GET', 'POST'])
def login():
    return login_handler(request)


@app.route('/logout')
def logout():
  return logout_handler()


@app.route('/protected', methods=["GET"])
@login_required
def protected():
    return render_template('protected.html')

@app.route('/post_recipe')
def post_recipe():
	return render_template("post.html")

@app.route('/recipes/<string:country_name>')
def country_recipes(country_name):
	
	


