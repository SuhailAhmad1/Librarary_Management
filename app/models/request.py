from app import db
from app.models.product import Category
from app.models.user import User 

class CategoryRequest(db.Model):
    __tablename__ = 'requests_category'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(100))
    request_data = db.Column(db.TEXT)
    status = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id'))  # Define foreign key constraint
    user = db.relationship(User, backref='requests_category')
    category_id = db.Column(db.Integer, db.ForeignKey(
        'category.id'))  # Define foreign key constraint
    category = db.relationship(Category, backref='requests_category')
