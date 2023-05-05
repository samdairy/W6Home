from flask_sqlalchemy import SQLAlchemy

# import uuid library from Python (universal unique identifier)
import uuid

from datetime import datetime

# Adding Flask Security for Passwords
from werkzeug.security import generate_password_hash, check_password_hash

# Import for Secrets Module (Provided by Python)
import secrets

# Imports for Login Manager and the UserMixin
from flask_login import LoginManager, UserMixin

# Import for Flask-Marshmallow
from flask_marshmallow import Marshmallow

# Step 2 is passing this database reference to init.py
db = SQLAlchemy()
login_manager = LoginManager()

ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# Step 1
# This class will create the database table for us
class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(150), nullable = True, default = '')
    last_name = db.Column(db.String(150), nullable = True, default ='')
    
    # nullable = False means that it cannot be empty
    email = db.Column(db.String(150), nullable = False)
    
    # No limit on the password length. We will encrypt this
    password = db.Column(db.String, nullable = False, default = '')
    
    # Unique = True means that nothing can be duplicated within a token
    token = db.Column(db.String, default ='', unique = True)
    date_create = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    car = db.relationship('Car',backref = 'owner', lazy = True)

    def __init__(self, email,first_name = '', last_name='', id = '', password = '', token = ''):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)

    # Used for authentication for users to view only their cars
    def set_token(self,length):
        return secrets.token_hex(length)

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return f'User {self.email} has been created and added to database!'


class Car(db.Model):
    id = db.Column(db.String, primary_key = True)
    make = db.Column(db.String(150))
    model = db.Column(db.String(200), nullable = True)
    # Precision means we will have 10 available spaces for numeric value with 2 decimal places at the end of it
    sale_price = db.Column(db.Numeric(precision=10, scale = 2))
    color = db.Column(db.String(150))
    year = db.Column(db.Numeric(precision=4))
    mpg = db.Column(db.String(100))
    new_used = db.Column(db.String(20))
    # Specify Foriegn Key relationship in the () after db.ForeignKey
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    # id goes at the end of the list
    def __init__(self, make, model, sale_price, color, year, mpg, new_used, user_token, id = ''):
        self.id = self.set_id()
        self.make = make
        self.model = model
        self.sale_price = sale_price
        self.color = color
        self.year = year
        self.mpg = mpg
        self.new_used = new_used
        self.user_token = user_token

    def __repr__(self):
        return f'The following Car has been added: {self.name}'

    def set_id(self):
        return secrets.token_urlsafe()


class CarSchema(ma.Schema):
    class Meta:
        # Don't want to expose the token for the user, so not included here
        # This is what we should see as the end result of the json in Insomnia
        # Asking the Schema to create the look and feel of our results
        fields = ['id', 'make', 'model', 'sale_price', 'color', 'year', 'mpg', 'new_used']

car_schema = CarSchema()
# many = True means it should display the results in a list if many cars are available/entered
cars_schema = CarSchema(many = True)