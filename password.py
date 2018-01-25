from flask_login import UserMixin

from sqlalchemy import Column, DateTime, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

from werkzeug.security import generate_password_hash, check_password_hash

Base = declarative_base()


class User(UserMixin, Base):
    __tablename__ = 'user'
    id            = Column(Integer, primary_key=True)
    email         = Column(String)
    pw_hash       = Column(String)
    authenticated = Column(Boolean, default=False)

    def __repr__(self):
      return "<User: %s, password: %s>" % (
        self.email, self.pw_hash)

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)


class recommendation(Base):
    __tablename__ = 'recommendation'
    id            = Column(Integer, primary_key=True)
    owner         = Column(Integer, ForeignKey('user.id'))
    title         = Column(String)
    genre       = Column(String)
    recommendation   = Column(String)
    picture_url   = Column(String)
    summary  = Column(String)


# IF YOU NEED TO CREATE OTHER TABLE 
# FOLLOW THE SAME STRUCTURE AS YourModel