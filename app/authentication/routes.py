from flask import Blueprint, render_template, request, url_for, flash, redirect, jsonify
from app.models import User, db, check_password_hash
from app.signupform import UserSignUp
from app.signinform import UserSignin
from flask_login import login_user, logout_user, LoginManager, current_user, login_required
from sqlalchemy.exc import SQLAlchemyError
import secrets

auth = Blueprint('auth', __name__, template_folder='auth_templates')

# Route to get user token (requires authentication)
@auth.route('/api/user/token', methods=['GET'])
@login_required
def get_user_token():
    return jsonify({'token': current_user.token})

# Route for user registration
@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = UserSignUp()

    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            first_name = form.first_name.data
            last_name = form.last_name.data

            existing_login = User.query.filter_by(email=email).first()

            if existing_login:
                flash('User is already registered for this website. Use a different email.', 'user-exists')
                return redirect(url_for('auth.signup'))

            # Generate a token for the newly signed-up user
            user_token = secrets.token_hex(16)

            user = User(email=email, first_name=first_name, last_name=last_name, password=password, token=user_token)
            db.session.add(user)
            db.session.commit()

            # Update the user's token in the database
            user.token = user_token
            db.session.commit()

            flash(f"You've successfully created an account {first_name}! Welcome to my website, poke around!", 'user-created')

            # Pass the current_user to the template
            return render_template('signup.html', form=form, user_token=user_token, current_user=current_user)
    except Exception as e:
        print(f'Error: {e}')
        flash(f"An error has occurred. Please try again", 'auth-failed')

    return render_template('signup.html', form=form)

# Route for user login
@auth.route('/signin', methods=['GET', 'POST'])
def signin():
    form = UserSignin()

    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            
            logged_user = User.query.filter(User.email == email).first()
            if logged_user and check_password_hash(logged_user.password, password):
                login_user(logged_user)
                flash('Welcome!', 'auth-success')
                return redirect(url_for('site.home'))
            else:
                flash(f"The login attempt has failed",'auth-failed')
                return redirect(url_for('auth.signin'))
    except SQLAlchemyError as e:
        print(f'SQLAlchemyError: {e}')
        flash(f"An error has occurred. Please try again", 'auth-failed')  
    return render_template("signin.html", form=form)

# Route for user logout
@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('site.home'))
