from pre_owned_books.users.forms import RegistrationForm
from pre_owned_books import db, app
from flask import render_template, Blueprint
from pre_owned_books.models import User

users_blueprint = Blueprint('users_blueprint', __name__, url_prefix='/users')


@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    app.logger.info("Reached registration form...........")

    # If form is submitted (POST request), add user to DB after validations
    if form.validate_on_submit():
        app.logger.info("SUBMITTED registration form...........")
        username = form.username.data
        password = form.password.data
        new_user = User(username, password)
        db.session.add(new_user)
        db.session.commit()
        app.logger.info("Added a User...........")

    # if request method is 'GET', return registration form
    return render_template('users/register.html', form=form)

@users_blueprint.route('/all_users')
def all_users():
    user_list_string = '[ '
    for i in User.query.all():
        user_list_string = user_list_string + i.username + ', '
    user_list_string += ']'
    return user_list_string
