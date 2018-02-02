# flask imports
from flask import Flask, Response, render_template, request, redirect, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey

# flask setup
app = Flask(__name__)
app.config ['SQLALCHEMY_DATABASE_URI']= 'sqlite:///./test1.db'
db = SQLAlchemy(app)
session=db.session
# flask-login imports

class User(db.Model):
    __tablename__ = 'user'
    id            = db.Column(db.Integer, primary_key=True)
    email         = db.Column(db.String)
    pw_hash       = db.Column(db.String)
    authenticated = db.Column(db.Boolean, default=False)

    def __repr__(self):
      return "<User: %s, password: %s>" % (
        self.email, self.pw_hash)

    def set_password(self, password):
        self.pw_hash = password

    def check_password(self, password):
        return self.pw_hash == password


class Recommendation(db.Model):
    __tablename__ = 'recommendation'
    id            = db.Column(db.Integer, primary_key=True)
    owner         = db.Column(db.Integer, ForeignKey('user.id'))
    title         = db.Column(db.String)
    genre       = db.Column(db.String)
    recommendation   = db.Column(db.String)
    picture_url   = db.Column(db.String)
    summary  = db.Column(db.String)

db.create_all()

# we need this library for HTML-safe string operations
import cgi



@app.route('/')
def index():
	return render_template('home.html')
	
@app.route('/login', methods=['GET', 'POST'])
def login():
		return login_handler(request)


@app.route('/logout')
def logout():
	return logout_handler()


@app.route('/protected', methods=["GET"])
def protected():
		return render_template('protected.html')

@app.route('/post', methods=['GET','POST'])
def post_recommendation():
		if request.method == 'GET':
				return render_template("post.html")

		else:
			#read form data
			new_user_name = request.form.get('user_name')
			new_genre = request.form.get('recommendation_genre')
			new_book_Name = request.form.get('book_name')
			new_Pic_Of_book = request.form.get('Pic_Of_book')
			new_recommendation = request.form.get('recommendation')
			new_summary = request.form.get('summary')

			new_recommendation = (new_recommendation.replace('\n', '<br>'))

			post=Recommendation(owner=new_user_name,
			 genre=new_genre,
			 title=new_book_Name,
			 picture_url=new_Pic_Of_book,
			 recommendation=new_recommendation,
			 summary=new_summary)
			session.add(post)
			session.commit()

			# redirect user to the page that views all tweets
			return redirect(url_for('genre',genre=new_genre))

@app.route('/recommendation/<string:genre>')
def genre(genre):
	genre = genre.lower()
	r = Recommendation.query.filter_by(genre=genre).all()
	print (r)
	return render_template("genre.html", genre=genre, recommendations=r)

@app.route('/delete/<int:recommendation_id>', methods=['GET', 'POST'])
def delete_recommendation(recommendation_id):
		recommendation = session.query(recommendation).filter_by(id= recommendation_id).first()
		if request.method == 'GET':
			return render_template('delete.html', recommendation = recommendation)
		else:
			genre = recommendation.genre
			session.delete(recommendation)
			return redirect(url_for('genre', genre = genre))

app.run()