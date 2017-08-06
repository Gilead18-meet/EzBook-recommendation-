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

Base.metadata.create_all()

recipe1 = Recipe(owner = "Gilead", title ="amazing flour",country= "USA", ingredients = "flour", picture_url= "coming up", description = "mix flour")
session.add(recipe1)

session.commit()
