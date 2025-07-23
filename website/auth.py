# import external libraries
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
# import database
from . import db
# import from .models user
from .models import User
from .forms import RegistrationForm

# set auth blueprint
auth = Blueprint("auth", __name__)

# sign-up route
@auth.route("/sign-up", methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        # If user already logged in return to Home page
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(
            (form.password.data), method='scrypt:32768:8:1')  # Make password encrypted
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()  # Adds new user to database with all information submitted
        flash('Account created!', category='success')
        login_user(user, remember=True)
        return redirect(url_for('views.home'))  # Returns to Home page
    # Return to Signup page
    return render_template('sign_up.html', form=form, user=current_user)

# login route
@auth.route("/login", methods=['GET', 'POST'])
# login function
# returns login.html
def login():
    # gets email and password from login form
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        # queries database to recieve user information using email address
        user = User.query.filter_by(email=email).first()
        # checks email and password
        if user:
            # if correct log in user and redurect to home page
            if check_password_hash(user.password, password):
                flash("Logged in successfully!", category="success")
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            # if incorrect password flash error
            else:
                flash("Incorrect password.", category="error")
        # if incorrect email flash error
        else:
            flash("Email does not exist.", category="error")
    return render_template("login.html", user=current_user)

# logout route
@auth.route("/logout")
@login_required
# logout function
# returns logout.html
def logout():
    logout_user()
    flash('Logged out successfully!', category='success')
    return redirect(url_for('views.home'))