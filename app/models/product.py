from app import db
from app.models.user import User

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    rate = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    is_active = db.Column(db.Integer)
    userid = db.Column(db.Integer, db.ForeignKey('users.id'))  # Define foreign key constraint
    user = db.relationship(User, backref='products')
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))  # Define foreign key constraint
    category = db.relationship('Category', backref='products')

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    is_active = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # Define foreign key constraint
    user = db.relationship(User, backref='category')

class UserCart(db.Model):
    __tablename__ = 'user_cart'
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer)
    amount = db.Column(db.Integer)
    rate = db.Column(db.Integer)
    notes = db.Column(db.String(300))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # Define foreign key constraint
    user = db.relationship(User, backref='user_cart')
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))  # Define foreign key constraint
    product = db.relationship('Product', backref='user_cart')

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer)
    amount = db.Column(db.Integer)
    rate = db.Column(db.Integer)
    notes = db.Column(db.String(300))
    address = db.Column(db.String(200))
    status = db.Column(db.String(100))
    full_name = db.Column(db.String(100))
    phone_number = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # Define foreign key constraint
    user = db.relationship(User, backref='orders')
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))  # Define foreign key constraint
    product = db.relationship('Product', backref='orders')
