from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import os




db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://myuser:kristi@localhost/ecommerce_db'
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['LOGIN_VIEW'] = 'login'  # Route da cui reindirizzare gli utenti non autenticati
    app.config['UPLOAD_FOLDER'] = 'static'
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Importa e inizializza le route
    from app.routes import init_routes
    init_routes(app)

    return app
