from flask import Blueprint
from app.controllers.admin_controller import get_all_requests, update_request

admin_routes = Blueprint('admin', __name__, url_prefix="/api/admin")

admin_routes.route("/get_all_requests", methods=["GET"])(get_all_requests)
admin_routes.route("/update_request", methods=["PUT"])(update_request)