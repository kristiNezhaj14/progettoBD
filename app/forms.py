from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User, Vendor

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class VendorRegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    piva = StringField('Partita IVA', validators=[DataRequired()])
    nome_azienda = StringField('Nome Azienda', validators=[DataRequired()])
    indirizzo = StringField('Indirizzo', validators=[DataRequired()])
    città = StringField('Città', validators=[DataRequired()])
    nazione = StringField('Nazione', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_username(self, username):
        vendor = Vendor.query.filter_by(username=username.data).first()
        if vendor is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        vendor = Vendor.query.filter_by(email=email.data).first()
        if vendor is not None:
            raise ValidationError('Please use a different email address.')
