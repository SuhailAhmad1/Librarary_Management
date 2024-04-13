from flask import Blueprint
from app.controllers.auth_controller import login, signup, refresh_token
auth_routes = Blueprint('auth', __name__, url_prefix="/api/auth")

auth_routes.route("/signup", methods=["POST"])(signup)
auth_routes.route('/login', methods=['POST'])(login)
auth_routes.route('/refresh_token', methods=["GET"])(refresh_token)
