from flask import Blueprint
from app.controllers.manager_controller import get_all_products, add_product, edit_product, delete_product, \
    add_category, delete_category, edit_category, get_manager_orders, update_order_status, get_manager_statistics, \
    get_manager_requests, trigger_generate_csv, read_gen_task_status, download_csv

manager_routes = Blueprint('manager', __name__, url_prefix="/api/manager")

manager_routes.route("/add_category", methods=["POST"])(add_category)
manager_routes.route("/delete_category/<int:cat_id>", methods=["DELETE"])(delete_category)
manager_routes.route("/edit_category", methods=["POST"])(edit_category)
manager_routes.route("/get_all_products", methods=["GET"])(get_all_products)
manager_routes.route("/add_product", methods=["POST"])(add_product)
manager_routes.route("/edit_product", methods=["POST"])(edit_product)
manager_routes.route("/delete_product/<int:product_id>", methods=["DELETE"])(delete_product)
manager_routes.route("/get_manager_orders", methods=["GET"])(get_manager_orders)
manager_routes.route("/update_order_status", methods=["PUT"])(update_order_status)
manager_routes.route("/get_statistics", methods=["GET"])(get_manager_statistics)
manager_routes.route("/get_manager_requests", methods=["GET"])(get_manager_requests)
manager_routes.route("/generate_csv", methods=["GET"])(trigger_generate_csv)
manager_routes.route("/get_generate_task_status/<string:task_id>")(read_gen_task_status)
manager_routes.route("/download_csv", methods=["POST"])(download_csv)