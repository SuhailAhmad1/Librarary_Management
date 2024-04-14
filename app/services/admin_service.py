from app.models.product import Product, Category, Order
from app.models.request import CategoryRequest
from app import db
import matplotlib.pyplot as plt
import os
import time
import json
from app.services.jobs import send_email_task


class AdminService:
    def get_all_requests_db(self):
        all_cat_requests = CategoryRequest.query.order_by(
            CategoryRequest.id.desc()).all()
        
        res = {
            "category_requests": []
        }
        for cat_request in all_cat_requests:
            res["category_requests"].append({
                "id": cat_request.id,
                "type": cat_request.type,
                "manager": cat_request.user.email,
                "request_data": json.loads(cat_request.request_data) if cat_request.request_data else "",
                "status": "Approved" if cat_request.status == 1 else "Rejected" if cat_request.status == -1 else "Pending",
                "category": cat_request.category.name if cat_request.category else ""
            })
        return res

    def update_request_status(self, data):
        manager_email = ""
        update_status = ""
        category_req = CategoryRequest.query.filter_by(
            id=data["request_id"]).first()
        if category_req:
            manager_email = category_req.user.email
            if data["status"] == -1:
                category_req.status = -1
                update_status = "Rejected"
            else:
                update_status = "Accepted"
                operation = category_req.type
                if operation == "CREATE":
                    cat_info = json.loads(category_req.request_data)
                    new_category = Category(
                        name=cat_info["category_name"],
                        description = cat_info["description"],
                        user_id=category_req.user_id,
                        is_active=1
                    )
                    db.session.add(new_category)

                elif operation == "DELETE":
                    all_products = Product.query.filter_by(
                        category_id=category_req.category_id, userid=category_req.user_id)
                    for product in all_products:
                        product.is_active = 0
                    category = Category.query.filter_by(
                        id=category_req.category_id, user_id=category_req.user_id).first()
                    if category:
                        category.is_active = 0

                elif operation == "EDIT":
                    category = Category.query.filter_by(
                        id=category_req.category_id, user_id=category_req.user_id).first()
                    if category:
                        category.name = json.loads(category_req.request_data)[
                            "category_name"]
                        category.description = json.loads(category_req.request_data)[
                            "category_description"]

                category_req.status = 1

        db.session.commit()
        send_email_task.delay(
            manager_email,
            "Request Status Update",
            f"Your request has been {update_status}. Please check your dashboard for latest status"
        )
        return True
