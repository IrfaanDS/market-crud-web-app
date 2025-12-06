from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError

from market.db_connect import fetch_one


class RegisterForm(FlaskForm):

    def validate_username(self, username_to_check):
        result = fetch_one("SELECT id FROM users WHERE username=%s", (username_to_check.data,))
        if result:
            raise ValidationError("Username already exists! Please try a different username.")

    def validate_email_address(self, email_address_to_check):
        result = fetch_one("SELECT id FROM users WHERE email_address=%s", (email_address_to_check.data,))
        if result:
            raise ValidationError("Email address already exists! Please try a different one.")

    username = StringField("User Name:", validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField("Email Address:", validators=[Email(), DataRequired()])
    password1 = PasswordField("Password:", validators=[Length(min=6), DataRequired()])
    password2 = PasswordField("Confirm Password:", validators=[EqualTo("password1"), DataRequired()])
    submit = SubmitField("Create Account")


class LoginForm(FlaskForm):
    username = StringField("User Name:", validators=[DataRequired()])
    password = PasswordField("Password:", validators=[DataRequired()])
    submit = SubmitField("Sign in")


class PurchaseItemForm(FlaskForm):
    submit = SubmitField("Purchase Item!")


class SellItemForm(FlaskForm):
    submit = SubmitField("Sell Item!")
