from flask import Blueprint
from app.controllers.user_controller import get_all_items, add_to_user_request, \
    get_my_books, get_user_items, get_user_book, return_book
user_routes = Blueprint('user', __name__, url_prefix="/api/user")

user_routes.route("/get_all_items", methods=["GET"])(get_all_items)
user_routes.route("/add_to_requests", methods=["POST"])(add_to_user_request)
user_routes.route("/get_all_user_requests", methods=["GET"])(get_user_items)
user_routes.route("/get_my_books", methods=["GET"])(get_my_books)
user_routes.route("/get_book/<int:product_id>", methods=["GET"])(get_user_book)
user_routes.route("/return_book/<int:request_id>", methods=["PUT"])(return_book)