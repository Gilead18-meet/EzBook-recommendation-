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


recipe1 = Recipe(name_of_publisher = "Gilead", name_of_recipe ="amazing flour",country= "USA", ingredients = "flour", picture= "coming up", how_to_make = "mix flour")
session.add(recipe1)

session.commit()

r = session.query(Recipe).filter_by(id = 1).first()
print(r.name_of_publisher)