import traceback
from passlib.hash import pbkdf2_sha256 as sha256
from flask import request, send_file
from app.services.manager_service import ManagerService
from app.services.auth_service import AuthService
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.jobs import generate_csv


manager_service = ManagerService()
auth_service = AuthService()


@jwt_required()
def get_manager_requests():
    try:
        userId = get_jwt_identity()
        if not auth_service.check_if_manager(userId):
            return {"message": "Unauthorized user"}, 403

        data = manager_service.get_all_requests_db(userId)
        if not data == False:
            return {"data": data}, 200
        return {"message": "something went wrong"}, 500
    except Exception as e:
        traceback.print_exc(e)
        return {"message": "Something went wrong"}, 500


@jwt_required()
def add_category():
    try:
        userId = get_jwt_identity()
        if not auth_service.check_if_manager(userId):
            return {"message": "Unauthorized user"}, 403
        content_type = request.headers.get("Content-Type")
        if not content_type == "application/json":
            return {"message": 'Only JSON allowed'}, 400

        data = request.get_json()

        if not ("category_name" in data and "description" in data):
            print(data)
            return {"message": 'Missing data in the request'}, 400
        status = manager_service.add_category_db(userId, data)
        if status:
            return {"message": "successfully added the category"}, 200
        return {"message": "something went wrong"}, 500
    except Exception as e:
        traceback.print_exc(e)
        return {"message": "Something went wrong"}, 500


@jwt_required()
def edit_category():
    try:
        userId = get_jwt_identity()
        if not auth_service.check_if_manager(userId):
            return {"message": "Unauthorized user"}, 403
        content_type = request.headers.get("Content-Type")
        if not content_type == "application/json":
            return {"message": 'Only JSON allowed'}, 400

        data = request.get_json()

        if not ("category_name" in data and "category_id" in data and "category_description" in data):
            return {"message": 'Missing data in the request'}, 400
        status = manager_service.edit_category_db(userId, data)
        if status:
            return {"message": "successfully updated the category"}, 200
        return {"message": "something went wrong"}, 500

    except Exception as e:
        traceback.print_exc(e)
        return {"message": "Something went wrong"}, 500


@jwt_required()
def delete_category(cat_id):
    try:
        userId = get_jwt_identity()
        if not auth_service.check_if_manager(userId):
            return {"message": "Unauthorized user"}, 403
        status = manager_service.delete_category_db(userId, cat_id)
        if status:
            return {"message": "successfully deleted the category"}, 200
        return {"message": "something went wrong"}, 500

    except Exception as e:
        traceback.print_exc(e)
        return {"message": "Something went wrong"}, 500


@jwt_required()
def get_all_products():
    try:
        userId = get_jwt_identity()
        if not auth_service.check_if_manager(userId):
            return {"message": "Unauthorized user"}, 403
        products = manager_service.get_all_products_db(userId)
        return {"data": products}, 200
    except Exception as e:
        traceback.print_exc(e)
        return {"message": "Something went wrong"}, 500


@jwt_required()
def add_product():
    try:
        userId = get_jwt_identity()
        if not auth_service.check_if_manager(userId):
            return {"message": "Unauthorized user"}, 403
        print(request.files)
        if 'file' not in request.files:
            return {"message": "Please attach a file"}, 400
        data = {
            "book_name" : request.form['name'],
            "author": request.form["author"],
            "category_id" : request.form["category_id"]
        }
        file = request.files["file"]

        status = manager_service.add_product_db(userId, data, file)
        if status:
            return {"message": "successfully added the item"}, 200
        return {"message": "something went wrong"}, 500
    except Exception as e:
        traceback.print_exc(e)
        return {"message": "Something went wrong"}, 500


@jwt_required()
def edit_product():
    try:
        userId = get_jwt_identity()
        if not auth_service.check_if_manager(userId):
            return {"message": "Unauthorized user"}, 403
        content_type = request.headers.get("Content-Type")
        if not content_type == "application/json":
            return {"message": 'Only JSON allowed'}, 400

        data = request.get_json()

        if not ("product_id" in data and "name" in data and "author" in data):
            return {"message": 'Missing data in the request'}, 400
        status = manager_service.edit_product_db(userId, data)
        if status:
            return {"message": "successfully updated the item"}, 200
        return {"message": "something went wrong"}, 500

    except Exception as e:
        traceback.print_exc(e)
        return {"message": "Something went wrong"}, 500


@jwt_required()
def delete_product(product_id):
    try:
        userId = get_jwt_identity()
        if not auth_service.check_if_manager(userId):
            return {"message": "Unauthorized user"}, 403
        status = manager_service.delete_product_db(userId, product_id)
        if status:
            return {"message": "successfully deleted the item"}, 200
        return {"message": "something went wrong"}, 500

    except Exception as e:
        traceback.print_exc(e)
        return {"message": "Something went wrong"}, 500


@jwt_required()
def get_book(product_id):
    try:
        userId = get_jwt_identity()
        if not auth_service.check_if_manager(userId):
            return {"message": "Unauthorized user"}, 403

        book_path = manager_service.get_book_path(product_id, userId)
        return send_file(book_path, as_attachment=True)

    except Exception as e:
        traceback.print_exc(e)
        return {"message": "Something went wrong"}, 500

@jwt_required()
def get_alluser_requets():
    try:
        userId = get_jwt_identity()
        if not auth_service.check_if_manager(userId):
            return {"message": "Unauthorized user"}, 403
        user_orders = manager_service.get_man_user_requests_db(userId)
        return {"data": user_orders}, 200
    except Exception as e:
        traceback.print_exc(e)
        return {"message": "Something went wrong"}, 500


@jwt_required()
def update_user_request_status():
    try:
        userId = get_jwt_identity()
        if not auth_service.check_if_manager(userId):
            return {"message": "Unauthorized user"}, 403
        content_type = request.headers.get("Content-Type")
        if not content_type == "application/json":
            return {"message": 'Only JSON allowed'}, 400

        data = request.get_json()

        if not ("request_id" in data and "status" in data):
            return {"message": 'Missing data in the request'}, 400
        status = manager_service.update_user_req_status_db(
            data["request_id"], data["status"])
        if status:
            return {"message": "successfully updated the order"}, 200
        return {"message": "something went wrong"}, 500

    except Exception as e:
        traceback.print_exc(e)
        return {"message": "Something went wrong"}, 500


@jwt_required()
def get_manager_statistics():
    try:
        userId = get_jwt_identity()
        if not auth_service.check_if_manager(userId):
            return {"message": "Unauthorized user"}, 403
        graph = manager_service.get_graph(userId)
        return send_file(graph, as_attachment=True)
    except Exception as e:
        traceback.print_exc(e)
        return {"message": "Something went wrong"}, 500


@jwt_required()
def trigger_generate_csv():
    try:
        userId = get_jwt_identity()
        if not auth_service.check_if_manager(userId):
            return {"message": "Unauthorized user"}, 403
        task = generate_csv.delay(userId)
        return {"data": str(task.id)}, 200
    except Exception as e:
        traceback.print_exc(e)
        return {"message": "Something went wrong"}, 500


@jwt_required()
def read_gen_task_status(task_id):
    try:
        userId = get_jwt_identity()
        if not auth_service.check_if_manager(userId):
            return {"message": "Unauthorized user"}, 403
        task = generate_csv.AsyncResult(task_id)
        if task.state == "SUCCESS":
            return {"status": task.state, "result": task.result}
        elif task.state == "PENDING":
            return {"status": task.state, "result": "Task pending"}
        elif task.state == "FAILURE":
            return {"status": task.state, "result": task.result}
        else:
            return {"status": task.state, "result": "Task in progress"}

    except Exception as e:
        traceback.print_exc(e)
        return {"message": "Something went wrong"}, 500


@jwt_required()
def download_csv():
    try:
        userId = get_jwt_identity()
        if not auth_service.check_if_manager(userId):
            return {"message": "Unauthorized user"}, 403

        content_type = request.headers.get("Content-Type")
        if not content_type == "application/json":
            return {"message": 'Only JSON allowed'}, 400

        data = request.get_json()

        if not ("csv_data" in data):
            return {"message": 'Missing data in the request'}, 400

        csv_file = manager_service.create_csv(data["csv_data"], userId)
        return send_file(csv_file, as_attachment=True)

    except Exception as e:
        traceback.print_exc(e)
        return {"message": "Something went wrong"}, 500
