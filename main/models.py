from main import db,bcrypt,loginmanager
from sqlalchemy import ForeignKey, Integer,String, null
from flask_login import UserMixin

@loginmanager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model,UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=20), nullable=False)
    lastname = db.Column(db.String(length=20), nullable=False)
    email = db.Column(db.String(length=50), nullable=False) 
    address = db.Column(db.Text())
    number = db.Column(db.String(length=20))
    role = db.Column(db.Integer(), default=0)
    password_hash = db.Column(db.String(length=100), nullable=False)
    company = db.Column(db.String(length=50))
    img = db.Column(db.String(length=50))
    userName = db.relationship('Product', backref='user')

    @property   
    def password(self):
        return self.password
    
    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self,attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)


class Product(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=20))
    title = db.Column(db.String(length=20))
    about = db.Column(db.Text())
    photo_1 = db.Column(db.String(length=60))
    photo_2 = db.Column(db.String(length=50))
    stock = db.Column(db.Integer())
    product_code = db.Column(db.String(length=20))
    size = db.Column(db.String(length=20))
    price = db.Column(db.String(length=20))
    color = db.Column(db.String(length=20))
    control= db.Column(db.Integer(), default=0)
    req_cat = db.Column(db.String(length=20), default=null)
    category = db.Column(db.Integer(), ForeignKey('category.id'))
    stuff_user = db.Column(db.Integer(), ForeignKey('user.id'))
    cart = db.relationship('Carto', backref='product')

class Typec(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=50))
    categorys = db.relationship('Category', backref='typec')
    
class Category(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=50))
    type = db.Column(db.Integer(), ForeignKey('typec.id'))
    img = db.Column(db.String(length=100))

class Carto(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    productId = db.Column(db.Integer(), ForeignKey('product.id'))
    price = db.Column(db.Integer())
    seller = db.Column(db.Integer())
    pieces = db.Column(db.Integer(), default=1)
    userId = db.Column(db.Integer())
    sessionId = db.Column(db.String(length=200))
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())    












    







