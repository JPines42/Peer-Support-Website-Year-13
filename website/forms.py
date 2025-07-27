from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from .models import User


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=2, max=20)])  # Username must be between 2-20 characters
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=8, max=20)])  # Password must be between 8-20 characters
    confirm_password = PasswordField('Confirm Password', validators=[
                                     DataRequired(), EqualTo('password'), Length(min=8, max=20)])  # Confirming password
    submit = SubmitField('Sign Up')  # Submit to user database

    def validate_username(self, username):
        # If username is already in use
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                "Username already taken. Please choose a different one.")

    def validate_email(self, email):
        # If email is already in use
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                "Email already taken. Please choose a different one.")
