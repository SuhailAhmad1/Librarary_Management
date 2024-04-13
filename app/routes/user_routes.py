from flask import Blueprint
from app.controllers.user_controller import get_all_items, add_to_cart, get_cart_items, \
    edit_cart_item, delete_cart_item, place_order, get_user_orders
user_routes = Blueprint('user', __name__, url_prefix="/api/user")

user_routes.route("/get_all_items", methods=["GET"])(get_all_items)
user_routes.route("/add_to_cart", methods=["POST"])(add_to_cart)
user_routes.route("/get_all_cart_items", methods=["GET"])(get_cart_items)
user_routes.route("/edit_cart_item", methods=["POST"])(edit_cart_item)
user_routes.route("/delete_cart_item/<int:cart_id>", methods=["DELETE"])(delete_cart_item)
user_routes.route("/place_order", methods=["POST"])(place_order)
user_routes.route("/get_user_orders", methods=["GET"])(get_user_orders)