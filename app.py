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
def post_recommendation():
		if request.method == 'GET':
				return render_template("post.html")

		else:
			#read form data
			new_user_name = request.form.get('user_name')
			new_genre = request.form.get('genre')
			new_book_Name = request.form.get('book_name')
			new_Pic_Of_book = request.form.get('Pic_Of_book')
			new_recommendation = request.form.get('recommendation')
			new_summary = request.form.get('summary')

			new_recommendation = (new_recommendation.replace('\n', '<br>'))

			post=recommendation(owner=new_user_name,
			 genre=new_genre,
			 title=new_book_Name,
			 picture_url=new_Pic_Of_book,
			 recommendation=new_recommendation,
			 summary=new_summary)
			session.add(post)
			session.commit()

			# redirect user to the page that views all tweets
			return redirect(url_for('genre_page',genre=new_genre))


@app.route('/recommendation/<string:genre>')
def genre_page(genre):
	genre = genre.lower()
	r = session.query(recommendation).filter_by(genre=genre).all()
	return render_template("genre.html", genre=genre, recommendation=r)

@app.route('/delete/<int:recommendation_id>', methods=['GET', 'POST'])
def delete_recommendation(recommendation_id):
		recommendation = session.query(recommendation).filter_by(id= recommendation_id).first()
		if request.method == 'GET':
			return render_template('delete.html', recommendation = recommendation)
		else:
			genre = recommendation.genre
			session.delete(recommendation)
			return redirect(url_for('genre_page', genre = genre))