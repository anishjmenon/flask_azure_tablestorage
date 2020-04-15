from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DecimalField, SelectField, IntegerField
from wtforms.validators import DataRequired, Email

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    login = SubmitField('Login')

class StockConfirmationForm(FlaskForm):
    material = SelectField('Material', choices=[])
    quantity = IntegerField('Quantity', validators=[DataRequired(message='Please enter a number')])
    confirm = SubmitField('Confirm')