import traceback
from flask import request
from app.services.admin_service import AdminService
from app.services.auth_service import AuthService
from flask_jwt_extended import jwt_required, get_jwt_identity

admin_service = AdminService()
auth_service = AuthService()


@jwt_required()
def get_all_requests():
    try:
        userId = get_jwt_identity()
        if not auth_service.check_if_admin(userId):
            return {"message": "Unauthorized user"}, 403

        data = admin_service.get_all_requests_db()
        if not data == False:
            return {"data": data}, 200
        return {"message": "something went wrong"}, 500
    except Exception as e:
        traceback.print_exc(e)
        return {"message": "Something went wrong"}, 500



@jwt_required()
def update_request():
    try:
        userId = get_jwt_identity()
        if not auth_service.check_if_admin(userId):
            return {"message": "Unauthorized user"}, 403

        content_type = request.headers.get("Content-Type")
        if not content_type == "application/json":
            return {"message": 'Only JSON allowed'}, 400

        data = request.get_json()
        if not ("status" in data and "request_id" in data):
            return {"message": 'Missing data in the request'}, 400
        
        result = admin_service.update_request_status(data)
        if not result == False:
            return {"data": result}, 200
        return {"message": "something went wrong"}, 500
    except Exception as e:
        traceback.print_exc(e)
        return {"message": "Something went wrong"}, 500
