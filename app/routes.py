from flask import render_template
from app import app

@app.route('/')
def home():
    return render_template('TradeTrove/home.html')


@app.route('/login')
def login():
    return render_template('TradeTrove/login.html')

@app.route('/register')
def register():
    return render_template('TradeTrove/register.html')