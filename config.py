import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'
<<<<<<< HEAD
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://username:password@localhost/nome_del_database'
=======
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://myuser:kristi@localhost/ecommerce_db'
>>>>>>> 43afbf85f11838e078d4aa3734a285593be438b3
    SQLALCHEMY_TRACK_MODIFICATIONS = False
