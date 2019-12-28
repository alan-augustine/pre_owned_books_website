from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, EqualTo
from pre_owned_books.models import User
from wtforms import ValidationError


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
        if not User.query.filter_by(username=field.data):
            raise ValidationError("Username does not exists!")
