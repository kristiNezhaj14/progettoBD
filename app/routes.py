from flask import render_template, redirect, url_for, request, flash
from app import db
from app.models import User
from app.forms import RegistrationForm, LoginForm

def init_routes(app):
    @app.route('/')
    def home():
        return render_template('home.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            user = User.query.filter_by(username=username).first()
            if user and user.check_password(password):
                # Aggiungi la logica per la sessione utente qui
                flash('Login successful')
                return redirect(url_for('home'))
            else:
                flash('Login failed. Check your username and/or password.')
        return render_template('login.html', form=form)

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        form = RegistrationForm()
        if form.validate_on_submit():
            username = form.username.data
            email = form.email.data
            password = form.password.data
            
            # Verifica se l'username o l'email esistono già
            if User.query.filter_by(username=username).first():
                flash('Username already exists')
                return redirect(url_for('register'))

            if User.query.filter_by(email=email).first():
                flash('Email already registered')
                return redirect(url_for('register'))

            # Crea un nuovo utente e salva nel database
            new_user = User(username=username, email=email)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            flash('User registered successfully')
            return redirect(url_for('home'))

        return render_template('register.html', form=form)
