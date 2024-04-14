from app import db
from app.models.user import User


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    author = db.Column(db.String(100))
    book_path = db.Column(db.String(100))
    is_active = db.Column(db.Integer)
    userid = db.Column(db.Integer, db.ForeignKey('users.id')
                       )  # Define foreign key constraint
    user = db.relationship(User, backref='products')
    category_id = db.Column(db.Integer, db.ForeignKey(
        'category.id'))  # Define foreign key constraint
    category = db.relationship('Category', backref='products')


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(300))
    created_at = db.Column(db.DateTime,  default=db.sql.func.now())
    is_active = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id'))  # Define foreign key constraint
    user = db.relationship(User, backref='category')


class UserRequest(db.Model):
    __tablename__ = 'user_requests'
    id = db.Column(db.Integer, primary_key=True)
    days_requested = db.Column(db.Integer)
    status = db.Column(db.Integer)
    is_returned = db.Column(db.Integer, default=0)
    is_expired = db.Column(db.Integer, default=0)
    approved_at = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id'))  # Define foreign key constraint
    user = db.relationship(User, backref='user_requests')
    product_id = db.Column(db.Integer, db.ForeignKey(
        'products.id'))  # Define foreign key constraint
    product = db.relationship('Product', backref='user_requests')


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
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id'))  # Define foreign key constraint
    user = db.relationship(User, backref='orders')
    product_id = db.Column(db.Integer, db.ForeignKey(
        'products.id'))  # Define foreign key constraint
    product = db.relationship('Product', backref='orders')
