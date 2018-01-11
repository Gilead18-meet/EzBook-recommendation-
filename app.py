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

# we need this library for HTML-safe string operations
import cgi


@app.route('/')
def test_homepage():
	return render_template('home.html')


'''
@app.route('/post/<int:post_id>')
def post_recipe(post_id):
		recipe = session.query(Recipe).filter_by(id = post_id).first()
		return render_template('post.html', recipe = recipe)'''


'''
@app.route('/countries/<string:country>')
def country_page(country):
	recipes = session.query(Recipe).filter_by(country=country).all()
	return render_template('country.html', recipes=recipes, country=country)
'''
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

@app.route('/post_recommendation', methods=['GET','POST'])
def post_recipe():
		if request.method == 'GET':
				return render_template("post.html")

		else:
			#read form data
			new_user_name = request.form.get('user_name')
			new_genre = request.form.get('book_genre')
			new_book_Name = request.form.get('book_Name')
			new_Pic_Of_book = request.form.get('Pic_Of_book')
			new_recommendation = request.form.get('recommendation')
			new_description = request.form.get('description_of_book')

			new_recommendation = (new_recommendation.replace('\n', '<br>'))

			post=recommendation(owner=new_user_name,
			 genre=new_genre,
			 title=new_book_Name,
			 picture_url=new_Pic_Of_book,
			 recommendation=new_recommendation,
			 description=new_description)
			session.add(post)
			session.commit()

			# redirect user to the page that views all tweets
			return redirect(url_for('genre_page',genre=new_genre))


@app.route('/recommendation/<string:janer>')
def recommendation_page(recommendation):
	recommendation = recommendation.lower()
	r = session.query(genre).filter_by(recommendation=recommendation).all()
	return render_template("recommendation.html", recommendation=recommendation, genre=r)

@app.route('/delete/<int:recipe_id>', methods=['GET', 'POST'])
def delete_recipe(recipe_id):
		recipe = session.query(Recipe).filter_by(id= recipe_id).first()
		if request.method == 'GET':
			return render_template('delete.html', recipe = recipe)
		else:
			country = recipe.country
			session.delete(recipe)
			return redirect(url_for('country_page', country = country))