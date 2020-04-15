from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DecimalField, SelectField, IntegerField
from wtforms.validators import DataRequired, Email

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    login = SubmitField('Login')

class StockConfirmationForm(FlaskForm):
    material = StringField('Material', validators=[DataRequired()])
    # material = SelectField('Material', choices=[], coerce=int)
    quantity = IntegerField('Quantity', validators=[DataRequired(message='Please enter a number')])
    confirm = SubmitField('Confirm')