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
                flash('Username already exists', 'danger')
                return redirect(url_for('register'))

            if User.query.filter_by(email=email).first():
                flash('Email already registered', 'danger')
                return redirect(url_for('register'))

            # Crea un nuovo utente e salva nel database
            new_user = User(username=username, email=email)
            new_user.set_password(password)
            db.session.add(new_user)
            try:
                db.session.commit()
                flash('User registered successfully', 'success')
                return redirect(url_for('home'))
            except Exception as e:
                db.session.rollback()
                flash('An error occurred. Please try again.', 'danger')

        return render_template('register.html', form=form)
    
    @app.route('/categories')
    def categories():
        return render_template('categories.html')

    @app.route('/offersbanner')
    def offersbanner():
        return render_template('offersbanner.html')

    @app.route('/cart')
    def cart():
        return render_template('cart.html')
    

    @app.route('/contacts')
    def contacts():
        return render_template('contacts.html')
    
    @app.route('/faq')
    def faq():
        return render_template('faq.html')
    
    @app.route('/found')
    def found():
        return render_template('found.html')
    
    @app.route('/offers')
    def offers():
        return render_template('offers.html')
    
    
    @app.route('/product')
    def product():
        return render_template('product.html')
    
    @app.route('/terms')
    def terms():
        return render_template('terms.html')
    
    @app.route('/question')
    def question():
        return render_template('question.html')
    
    @app.route('/profile')
    def profile():
        return render_template('profile.html')
    
    @app.route('/productreg')
    def productreg():
        return render_template('productreg.html')
    
    @app.route('/vendor')
    def vendor():
        return render_template('vendor.html')
    
    @app.route('/vendorprofile')
    def vendorprofile():
        return render_template('vendorprofile.html')
    
