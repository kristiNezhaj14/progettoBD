from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, current_user, login_required
from app import db, login_manager
from app.models import User, Vendor,Product
from app.forms import RegistrationForm, LoginForm, VendorRegistrationForm

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def init_routes(app):
    @app.route('/')
    def home():
        return render_template('home.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        form = LoginForm()
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            user = User.query.filter_by(username=username).first()
            if user and user.check_password(password):
                login_user(user, remember=form.remember_me.data)
                flash('Login successful', 'success')
                return redirect(url_for('home'))
            else:
                flash('Login failed. Check your username and/or password.', 'danger')
        return render_template('login.html', form=form)

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash('You have been logged out.', 'info')
        return redirect(url_for('home'))

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        form = RegistrationForm()
        if form.validate_on_submit():
            username = form.username.data
            email = form.email.data
            password = form.password.data

            if User.query.filter_by(username=username).first():
                flash('Username already exists', 'danger')
                return redirect(url_for('register'))

            if User.query.filter_by(email=email).first():
                flash('Email already registered', 'danger')
                return redirect(url_for('register'))

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

    @app.route('/vendor', methods=['GET', 'POST'])
    def vendor():
        form = VendorRegistrationForm()
        if form.validate_on_submit():
            username = form.username.data
            email = form.email.data
            password = form.password.data
            piva = form.piva.data
            nome_azienda = form.nome_azienda.data
            indirizzo = form.indirizzo.data
            città = form.città.data
            nazione = form.nazione.data
            # Verifica se lo username o l'email sono già utilizzati da un utente
            if User.query.filter_by(username=username).first():
                flash('Username already exists in User accounts', 'danger')
                return redirect(url_for('vendor'))

            if User.query.filter_by(email=email).first():
                flash('Email already registered in User accounts', 'danger')
                return redirect(url_for('vendor'))
            # Verifica se lo username o l'email sono già utilizzati da un venditore
            if Vendor.query.filter_by(username=username).first():
                flash('Username already exists', 'danger')
                return redirect(url_for('vendor'))

            if Vendor.query.filter_by(email=email).first():
                flash('Email already registered', 'danger')
                return redirect(url_for('vendor'))

            new_vendor = Vendor(username=username, email=email, piva=piva, nome_azienda=nome_azienda, indirizzo=indirizzo, città=città, nazione=nazione)
            new_vendor.set_password(password)
            db.session.add(new_vendor)
            try:
                db.session.commit()
                flash('Vendor registered successfully', 'success')
                return redirect(url_for('home'))
            except Exception as e:
                db.session.rollback()
                flash('An error occurred. Please try again.', 'danger')

        return render_template('vendor.html', form=form)


    @app.route('/categories')
    def categories():
        return render_template('categories.html')

    @app.route('/offersbanner')
    def offersbanner():
        products = Product.query.all()
        return render_template('offersbanner.html',products=products)

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
    
    @app.route('/vendorprofile')
    def vendorprofile():
        return render_template('vendorprofile.html')


