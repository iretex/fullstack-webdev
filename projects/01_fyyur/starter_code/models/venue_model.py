# import sys
# sys.path.append('../')
# from sqlalchemy.orm import declarative_base, relationship
from database.postgres import db
# from show_model import Show

# Base = declarative_base()

class Venue(db.Model):
  __tablename__ = 'Venue'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)
  genres = db.Column(db.ARRAY(db.String()))
  address = db.Column(db.String(120))
  city = db.Column(db.String(120))
  state = db.Column(db.String(120))
  phone = db.Column(db.String(120))
  image_link = db.Column(db.String(500))
  facebook_link = db.Column(db.String(120))
  website_link = db.Column(db.String(120))
  seeking_talent = db.Column(db.Boolean)
  seeking_description = db.Column(db.String(500))
  shows = db.relationship('Show', backref='Venue', lazy=True)
  
  def __repr__(self):
      return '<Venue {}>'.format(self.name)

# TODO: implement any missing fields, as a database migration using Flask-Migrate