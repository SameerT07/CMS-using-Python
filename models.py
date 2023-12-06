from app import db
from flask_login import UserMixin

# User model for authentication
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    # Additional fields for user roles, profile, etc. can be added here

# Article model
# class Article(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(100), nullable=False)
#     content = db.Column(db.Text, nullable=False)
#     publication_date = db.Column(db.DateTime, nullable=False)
#     author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

#     # Add more fields like tags, attachments, etc.

#     # Define a relationship between the User and Article models
#     author = db.relationship('User', backref='articles')

# Additional models for tags, attachments, or other entities can be defined here

class User(db.Model, UserMixin):
    # ...
    role = db.Column(db.String(10), default='user', nullable=False)  # Default role is 'user'

from flask_uploads import UploadSet, configure_uploads, IMAGES, DOCUMENTS

# Define upload sets for images and documents
images = UploadSet('images', IMAGES)
documents = UploadSet('documents', DOCUMENTS)

class Article(db.Model):
    # ...
    image = db.Column(db.String(255))
    document = db.Column(db.String(255))
