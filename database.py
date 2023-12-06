from flask_sqlalchemy import SQLAlchemy
from app import app

# Configure the database URI. You can use other databases like PostgreSQL if needed.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'

# Create the SQLAlchemy database object
db = SQLAlchemy(app)

# Initialize the database with the Flask app
with app.app_context():
    db.init_app(app)

# Create the database tables based on the defined models
db.create_all()
