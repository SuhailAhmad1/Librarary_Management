import traceback
from passlib.hash import pbkdf2_sha256 as sha256
from flask import request
from app.services.auth_service import AuthService
from app.utils import build_cors_preflight_response
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from app.services.jobs import send_email_task

auth_service = AuthService()


def signup():
    try:
        if request.method == "OPTIONS":
            return build_cors_preflight_response()

        content_type = request.headers.get('Content-Type')
        if not (content_type == 'application/json'):
            return {"message": "Wrong input format, only JSON allowed"}, 400

        data = request.get_json()
        if not ("password" in data and "email" in data):
            return {"message": "Missing important information"}, 400

        if len(data["password"]) < 6:
            return {"message": "Password is too short"}, 400

        user = auth_service.get_user_by_email(data["email"])
        if user == False:
            return {"message": "Something went wrong"}, 500
        if not user:
            status = auth_service.create_new_user(data)
            if status:

                send_email_task.delay(data["email"], "Registration Done",
                                "Welcome to our Grocery Application. Your registration is succesfull")
                
                return {"message": "User created successfully"}, 200
            else:
                return {"message": "Something went wrong"}, 500
        else:
            return {"message": "User with this email already exists"}, 409

    except Exception as e:
        print(traceback.print_exc(e))
        return {"message": "Something went wrong"}, 500


def login():
    try:
        if request.method == "OPTIONS":
            return build_cors_preflight_response()

        content_type = request.headers.get('Content-Type')
        if not (content_type == 'application/json'):
            return {"message": "Wrong input format, only JSON allowed"}, 400

        data = request.get_json()
        if not ("email" in data and "password" in data):
            return {"message": "Missing important information"}, 400
        if not (data["email"] and data["password"]):
            return {"message": "Email and Password cannot be empty"}, 400

        user = auth_service.get_user_by_email(data["email"])
        if user == False:
            return {"message": "Something went wrong"}, 500
        if user and sha256.verify(data["password"], user["password"]):
            access_token = create_access_token(user["id"])
            refresh_token = create_refresh_token(user['id'])
            return {
                "user_id": user["id"],
                "user_name": user["username"],
                "user_role": user["user_role"],
                "access_token": access_token,
                "refresh_token": refresh_token
            }, 200
        else:
            return {"message": "Wrong crediantials"}, 401
    except Exception as e:
        print(traceback.print_exc(e))
        return {"message": "Something went wrong"}, 500


@jwt_required(refresh=True)
def refresh_token():
    try:
        if request.method == "OPTIONS":
            return build_cors_preflight_response()

        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return {'access_token': access_token}, 200
    except Exception as e:
        print(traceback.print_exc(e))
        return {"message": "Something went wrong"}, 500
