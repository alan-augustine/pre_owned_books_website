from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, EqualTo
from pre_owned_books.models import User
from wtforms import ValidationError
from pre_owned_books import app

class RegistrationForm(FlaskForm):
    username = StringField('User Name: ', validators=[DataRequired()])
    password = PasswordField('Password: ',
                             validators=[DataRequired(), EqualTo('password_confirm',
                                                                 message='Passwords must match')])
    password_confirm = PasswordField('Re-Enter Password: ', validators=[DataRequired()])
    submit = SubmitField('Register')

    # Field validations functions should have name validate_<field_name>
    # This is a requirement set by 'wtforms' package
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Username already taken..")


class LoginForm(FlaskForm):
    username = StringField("Username: ", validators=[DataRequired()])
    password = PasswordField("Password: ", validators=[DataRequired()])
    submit = SubmitField("Login!")

    def validate_username(self, field):
        # If user is not present in DB, deny login
        if not User.query.filter_by(username=field.data).first():
            raise ValidationError("Username does not exists!")

    # password validation is not like username validation
    # username field validation = simply take data in username textbox and check if it exists in DB
    # password field validation = check if username (in username text-field) corresponding to that password exists in DB
    #                             + validate password(in text-box) is correct
    # here, we use 'self.username.data' to refer to username corresponding to the password field
    # validate_username method is called by an object which has username parameter in it
    def validate_password(self, field):
        user = User.query.filter_by(username=self.username.data).first()
        # check password, but only if user exists
        # possible optimization - add a flag parameter to Login Form class
        # and set it to 1 in validate_username method, if user exists - this can reduce one query to DB in 'validate_password' method
        if user and not user.check_password(field.data):
            raise ValidationError("Wrong Password!")
