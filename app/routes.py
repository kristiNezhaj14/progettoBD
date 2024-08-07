from flask import render_template, redirect, url_for, request, flash
from app import app, db
from app.models import User
from app.forms import RegistrationForm, LoginForm

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('signup'))
        
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash('User registered successfully')
        return redirect(url_for('home'))
    return render_template('register.html', form=form)

@app.route('/home')
def home():
    return render_template('home.html')
