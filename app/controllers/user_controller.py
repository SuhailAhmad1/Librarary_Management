import traceback
from flask import request, send_file
from app.services.user_service import UserService
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.jobs import send_email_task

user_service = UserService()


@jwt_required()
def get_all_items():
    try:
        items = user_service.get_all_items_db()
        return {"data": items}, 200

    except Exception as e:
        traceback.print_exc(e)
        return {"message": "Something went wrong"}, 500


@jwt_required()
def add_to_user_request():
    try:
        userId = get_jwt_identity()

        content_type = request.headers.get("Content-Type")
        if not content_type == "application/json":
            return {"message": 'Only JSON allowed'}, 400

        data = request.get_json()

        if not ("no_of_days" in data and "product_id" in data):
            return {"message": 'Missing data in the request'}, 400
        status, message = user_service.add_user_request_db(userId, data)
        if status:
            return {"message": "successfully added to the Requests"}, 200
        return {"message":  message}, 422
    except Exception as e:
        traceback.print_exc(e)
        return {"message": "Something went wrong"}, 500


@jwt_required()
def get_user_items():
    try:
        userId = get_jwt_identity()

        request_items = user_service.get_user_requests_db(userId)
        return {"data": request_items}, 200
    except Exception as e:
        traceback.print_exc(e)
        return {"message": "Something went wrong"}, 500


@jwt_required()
def get_my_books():
    try:
        userId = get_jwt_identity()
        content_type = request.headers.get("Content-Type")
        if not content_type == "application/json":
            return {"message": 'Only JSON allowed'}, 400

        data = request.get_json()
        if not ("cart_id" in data and "quantity" in data and "amount" in data):
            return {"message": 'Missing data in the request'}, 400
        status = user_service.edit_cart_db(userId, data)
        if status:
            return {"message": "successfully updated the item"}, 200
        return {"message": "something went wrong"}, 500

    except Exception as e:
        traceback.print_exc(e)
        return {"message": "Something went wrong"}, 500


@jwt_required()
def get_my_books():
    try:
        userId = get_jwt_identity()

        user_orders = user_service.get_user_books_db(userId)
        return {"data": user_orders}, 200
    except Exception as e:
        traceback.print_exc(e)
        return {"message": "Something went wrong"}, 500

@jwt_required()
def get_user_book(product_id):
    try:
        userId = get_jwt_identity()

        book_path = user_service.get_book_path(product_id)
        return send_file(book_path, as_attachment=True)

    except Exception as e:
        traceback.print_exc(e)
        return {"message": "Something went wrong"}, 500
    

@jwt_required()
def return_book(request_id):
    try: 
        userId = get_jwt_identity()

        status = user_service.return_book_db(request_id, userId)
        if status:
            return {"message": "successfully updated the order"}, 200
        return {"message": "Something went wrong"}, 500

    except Exception as e:
        traceback.print_exc(e)
        return {"message": "Something went wrong"}, 500