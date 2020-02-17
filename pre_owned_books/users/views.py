from pre_owned_books.users.forms import RegistrationForm, LoginForm
from pre_owned_books import db, app
from flask import render_template, Blueprint, request, redirect, url_for
from pre_owned_books.models import User
from flask_login import login_user, logout_user, login_required

users_blueprint = Blueprint('users_blueprint', __name__, url_prefix='/users')


@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    app.logger.info("Reached registration form...........")

    # If form is submitted (POST request), add user to DB after validations
    if form.validate_on_submit():
        app.logger.info("SUBMITTED registration form...........")
        username = form.username.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        password = form.password.data
        age = form.age.data
        new_user = User(username, first_name, last_name, email, password, age)
        db.session.add(new_user)
        db.session.commit()
        app.logger.info("Added a User...........")

    # if request method is 'GET', return registration form
    return render_template('users/register.html', form=form)

@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Check if username exists in DB
        user = User.query.filter_by(username=form.username.data).first()
        app.logger.info("Trying to log in user ")

        # Check username was provided in form and check whether password is correct
        # check_password method is defined in User Model class
        if user is not None and user.check_password(form.password.data):
            login_user(user)
            app.logger.info("Successfully logged-in user: " + user.username)
            # If user was trying to access a URL that require login, Flask saves that URL as 'next'\
            # In that case, we first re-direct the user to login page and after a successful login,
            # we will redirect the user to initial requested page
            next_url = request.args.get('next')
            # TODO: what does not next[0]=='/'  means ?
            if next_url is  None:
                # Go to Home Page
                next_url = url_for('core_blueprint.index')
            return redirect(next_url)
        else:
            app.logger.info("Unable to login user")
    # If GET HTTP method
    return render_template('users/login.html', form=form)



# Below is just for debugging puposes
@users_blueprint.route('/all_users')
def all_users():
    user_list_string = '[ '
    for i in User.query.all():
        user_list_string = user_list_string + i.username + ', '
    user_list_string += ']'
    return user_list_string

@login_required
@users_blueprint.route('/logout')
def logout():
    logout_user()
    return render_template('users/logout.html')

@login_required
@users_blueprint.route('/profile')
def profile():
    return render_template('users/profile.html')