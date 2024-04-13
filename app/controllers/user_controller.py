import traceback
from flask import request
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
def add_to_cart():
    try:
        userId = get_jwt_identity()

        content_type = request.headers.get("Content-Type")
        if not content_type == "application/json":
            return {"message": 'Only JSON allowed'}, 400

        data = request.get_json()

        if not ("rate" in data and "product_id" in data and "quantity" in data and "amount" in data and "notes" in data):
            return {"message": 'Missing data in the request'}, 400
        status = user_service.add_cart_db(userId, data)
        if status:
            return {"message": "successfully added to the cart"}, 200
        return {"message": "something went wrong"}, 500
    except Exception as e:
        traceback.print_exc(e)
        return {"message": "Something went wrong"}, 500


@jwt_required()
def get_cart_items():
    try:
        userId = get_jwt_identity()

        cart_items = user_service.get_cart_db(userId)
        return {"data": cart_items}, 200
    except Exception as e:
        traceback.print_exc(e)
        return {"message": "Something went wrong"}, 500


@jwt_required()
def edit_cart_item():
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
def delete_cart_item(cart_id):
    try:
        userId = get_jwt_identity()
        status = user_service.delete_cart_db(userId, cart_id)
        if status:
            return {"message": "successfully deleted the cart item"}, 200
        return {"message": "something went wrong"}, 500

    except Exception as e:
        traceback.print_exc(e)
        return {"message": "Something went wrong"}, 500


@jwt_required()
def place_order():
    try:
        userId = get_jwt_identity()
        data = request.get_json()
        print(data)
        if not ("address" in data and "phone_number" in data and "full_name" in data):
            return {"message": 'Missing data in the request'}, 400

        status, user_email = user_service.place_order_db(userId, data)
        if not status:
            return {"message": "something went wrong"}, 500
        send_email_task.delay(
            user_email,
            "Order Placed Succefully",
            "Your orders has been successfully placed. Please check your dashboard for latest status "
        )
        return {"message": "successfully placed the order"}, 200

    except Exception as e:
        traceback.print_exc(e)
        return {"message": "Something went wrong"}, 500


@jwt_required()
def get_user_orders():
    try:
        userId = get_jwt_identity()

        user_orders = user_service.get_user_orders_db(userId)
        return {"data": user_orders}, 200
    except Exception as e:
        traceback.print_exc(e)
        return {"message": "Something went wrong"}, 500
