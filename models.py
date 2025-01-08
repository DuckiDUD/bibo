from werkzeug.security import generate_password_hash,check_password_hash

from ext import db
from flask_login import UserMixin

class Products(db.Model):
    id = db.Column(db.String(), primary_key=True)
    name = db.Column(db.String())
    description = db.Column(db.String())
    price = db.Column(db.Integer())
    tag = db.Column(db.String())
    image = db.Column(db.String())
    likes = db.Column(db.String())
    reviews = db.Column(db.String())
    author = db.Column(db.String())


class Users(db.Model, UserMixin):
    id = db.Column(db.String(), primary_key=True)
    name = db.Column(db.String())
    email = db.Column(db.String())
    password = db.Column(db.String())
    birthdate = db.Column(db.String())
    cart = db.Column(db.String())
    rank = db.Column(db.Integer())

    def __init__(self,name,id,email,password,birthdate,cart,rank):
        self.name = name
        self.id = id
        self.email = email
        self.password = generate_password_hash(password)
        self.birthdate = birthdate
        self.cart = cart
        self.rank = rank