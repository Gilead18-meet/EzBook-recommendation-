from sqlalchemy import Column, DateTime, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Recipe(Base):
    __tablename__  = 'recipe'
    id = Column(Integer, primary_key=True)
    # ADD YOUR FIELD BELOW ID
    name_of_publisher=Column(String)
    name_of_recipe=Column(String)
    country=Column(String)
    ingredients=Column(String)
    picture=Column(String)
    how_to_make=Column(String)


# IF YOU NEED TO CREATE OTHER TABLE 
# FOLLOW THE SAME STRUCTURE AS YourModel