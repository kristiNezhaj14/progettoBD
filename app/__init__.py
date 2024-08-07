# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://myuser:kristi@localhost/ecommerce_db'
    
    db.init_app(app)
    migrate.init_app(app, db)

    from app import models  # Assicurati che questo import funzioni senza problemi

    return app
