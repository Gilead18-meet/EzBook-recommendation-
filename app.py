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

@app.route('/post_recipe', methods=['GET','POST'])
def post_recipe():
		if request.method == 'GET':
				return render_template("post.html")

		else:
			#read form data
			new_user_name = request.form.get('user_name')
			new_country = request.form.get('Recipe_Country')
			new_Recipe_Name = request.form.get('Recipe_Name')
			new_Pic_Of_Dish = request.form.get('Pic_Of_Dish')
			new_ingredients = request.form.get('Ingredients')
			new_description = request.form.get('How_To_Make')

			new_ingredients = (new_ingredients.replace('\n', '<br>'))

			post=Recipe(owner=new_user_name,
			 country=new_country,
			 title=new_Recipe_Name,
			 picture_url=new_Pic_Of_Dish,
			 ingredients=new_ingredients,
			 description=new_description)
			session.add(post)
			session.commit()

			# redirect user to the page that views all tweets
			return redirect(url_for('country_page',country=new_country))


@app.route('/recipes/<string:country>')
def country_page(country):
	country = country.lower()
	r = session.query(Recipe).filter_by(country=country).all()
	return render_template("country.html", country=country, recipes=r)

@app.route('/delete/<int:recipe_id>', methods=['GET', 'POST'])
def delete_recipe(recipe_id):
		recipe = session.query(Recipe).filter_by(id= recipe_id).first()
		if request.method == 'GET':
			return render_template('delete.html', recipe = recipe)
		else:
			country = recipe.country
			session.delete(recipe)
			return redirect(url_for('country_page', country = country))