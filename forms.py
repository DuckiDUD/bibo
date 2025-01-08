from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, PasswordField, EmailField,TextAreaField,IntegerField, FileField, IntegerRangeField
from wtforms.validators import DataRequired, Length, Email, NumberRange


class RegisterForm(FlaskForm):
    name = StringField("Full Name", validators=[DataRequired(),Length(3,32)])
    email = EmailField("Email", validators=[DataRequired(),Email()])
    password = PasswordField("Password", validators=[DataRequired(),Length(8,16)])
    date = DateField("Birthday", validators=[DataRequired()])

    register = SubmitField("Sign Up")

class AuthForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(),Email()])
    password = PasswordField("Password", validators=[DataRequired(),Length(8,16)])

    register = SubmitField("Sign In")

class SellForm(FlaskForm):
    name = StringField("Product name",validators=[DataRequired(),Length(3,32)])
    description=TextAreaField("Product Description",validators=[DataRequired(),Length(16,128)])

    price = IntegerField("Price", validators=[DataRequired()])

    f1 = FileField(validators=[DataRequired()])
    sell = SubmitField("Publish Product")

class RevForm(FlaskForm):

    rate = IntegerRangeField("Rating",default=9,validators=[NumberRange(min=1, max=10)])
    review = TextAreaField("Review", validators=[DataRequired(), Length(16,128)])

    sub = SubmitField("Leave a review")