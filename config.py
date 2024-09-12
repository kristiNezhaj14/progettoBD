import os

class Config:
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://myuser:kristi@localhost/ecommerce_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
