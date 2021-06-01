from flask_wtf import FlaskForm
from flaskblog import db
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError



class RegistrationForm(FlaskForm):
    username = StringField('username', validators=[
                           DataRequired(), Length(min=2, max=20)])
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    confirm_password = PasswordField('confirm_password', validators=[
                                     DataRequired(), EqualTo('password')])
    submit = SubmitField('submit')

    def validate_username(self, username):
        
        from flaskblog.models import User
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                "This Username is already taken. Please try different one.")

    def validate_email(self, email):
        from flaskblog.models import User
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                "This Email is already taken. Please try different one.")


class LoginForm(FlaskForm):
    password = PasswordField('password', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(), Email()])
    # remember = BooleanField('remember me')
    submit = SubmitField('login up')

class ResetpasswordForm(FlaskForm):
    otp = StringField('otp', validators=[
                           DataRequired(), Length(min=2, max=20)])

    password = PasswordField('password', validators=[DataRequired()])
    confirm_password = PasswordField('confirm_password', validators=[
                                     DataRequired(), EqualTo('password')])
    submit = SubmitField('submit')


        