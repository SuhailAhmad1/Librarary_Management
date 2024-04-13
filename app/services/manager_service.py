from app.models.product import Product, Category, Order
from app.models.request import CategoryRequest
from app import db
import matplotlib.pyplot as plt
import os
import time
import json
import csv
from app.services.jobs import send_email_task


DOWNLOAD_DIR = os.getenv("DOWNLOAD_DIR")


class ManagerService:
    def get_all_requests_db(self, userId):
        all_cat_requests = CategoryRequest.query.filter_by(
            user_id=userId).order_by(CategoryRequest.id.desc())

        res = {
            "category_requests": []
        }
        for cat_request in all_cat_requests:
            res["category_requests"].append({
                "id": cat_request.id,
                "type": cat_request.type,
                "status": "Approved" if cat_request.status == 1 else "Rejected" if cat_request.status == -1 else "Pending",
                "category": cat_request.category.name if cat_request.category else ""
            })

        return res

    def add_category_db(self, userId, data):
        new_request = CategoryRequest(
            type="CREATE",
            user_id=userId,
            status=0,
            request_data=json.dumps(data)
        )
        db.session.add(new_request)
        db.session.commit()
        return True

    def delete_category_db(self, userId, cat_id):
        new_request = CategoryRequest(
            type="DELETE",
            user_id=userId,
            status=0,
            request_data="",
            category_id=cat_id
        )
        db.session.add(new_request)
        db.session.commit()
        return True

    def edit_category_db(self, userId, data):
        new_request = CategoryRequest(
            type="EDIT",
            user_id=userId,
            status=0,
            request_data=json.dumps(data),
            category_id=data["category_id"]
        )
        db.session.add(new_request)
        db.session.commit()
        return True

    def get_all_products_db(self, userid):
        manager_categories = Category.query.filter_by(
            user_id=userid, is_active=1).order_by(Category.id.desc())
        res = []
        for cat in manager_categories:
            this_cart = {
                "cat_id": cat.id,
                "cat_name": cat.name,
                "products": []
            }
            products = Product.query.filter_by(
                category_id=cat.id, is_active=1).order_by(Product.id.desc())
            for pro in products:
                this_pro = {
                    "id": pro.id,
                    "itemName": pro.name,
                    "rate": pro.rate,
                    "quantity": pro.quantity,
                }
                this_cart["products"].append(this_pro)
            res.append(this_cart)
        return res

    def add_product_db(self, userId, data):
        new_product = Product(
            name=data["name"],
            rate=data["rate"],
            quantity=data["quantity"],
            userid=userId,
            category_id=data["category_id"],
            is_active=1
        )
        db.session.add(new_product)
        db.session.commit()
        return True

    def edit_product_db(self, userId, data):
        product = Product.query.filter_by(
            id=data["product_id"], userid=userId).first()
        if product:
            product.name = data["name"]
            product.rate = data["rate"]
            product.quantity = data["quantity"]
            db.session.commit()
            return True
        else:
            return False

    def delete_product_db(self, userId, product_id):
        product = Product.query.filter_by(id=product_id, userid=userId).first()
        if product:
            product.is_active = 0
            db.session.commit()
            return True
        return False

    def get_manager_orders_db(self, userId):
        orders = Order.query.join(Order.product).filter(
            Product.userid == userId).order_by(Order.id.desc())

        res = []
        for order in orders:
            this_order = {
                "id": order.id,
                "product_name": order.product.name,
                "amount": order.amount,
                "address": order.address,
                "phone_number": order.phone_number,
                "quantity": order.quantity,
                "status": order.status,
                "name": order.full_name
            }
            res.append(this_order)
        return res

    def update_order_status_db(self, order_id, new_status):
        order = Order.query.filter_by(id=order_id).first()
        if order:
            order.status = new_status
            db.session.commit()
            send_email_task.delay(
                order.user.email,
                "Order status update",
                f"Your orders has been successfully {new_status}. Please check your dashboard for latest status"
            )
            return True
        return False

    def get_graph(self, userId):
        products = Product.query.filter_by(
            userid=userId).order_by(Product.id.desc())
        product_name = []
        product_count = []
        for pro in products:
            order_count = Order.query.filter_by(product_id=pro.id)
            count = 0
            for c in order_count:
                count += 1
            this_product_name = pro.name
            cat = Category.query.filter_by(id=pro.category_id).first()
            this_product_name += "##" + (cat.name if cat else "del")
            product_name.append(this_product_name)
            product_count.append(count)
        plt.figure(figsize=(10, 6))
        plt.bar(product_name, product_count, color='skyblue')
        plt.xlabel('Products')
        plt.ylabel('Number of orders')
        plt.title('Products vs Orders')
        plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
        plt.tight_layout()

        # Save the plot as an image file
        if not os.path.isdir(DOWNLOAD_DIR):
            os.mkdir(DOWNLOAD_DIR)
        if not os.path.isdir(DOWNLOAD_DIR+str(userId)):
            os.mkdir(DOWNLOAD_DIR+str(userId))
        graph_path = f"{DOWNLOAD_DIR}{str(userId)}/statistics_chart.png"
        plt.savefig(graph_path)

        return graph_path


    def create_csv(self, data, userId):
        if not os.path.isdir(DOWNLOAD_DIR):
            os.mkdir(DOWNLOAD_DIR)
        if not os.path.isdir(DOWNLOAD_DIR+str(userId)):
            os.mkdir(DOWNLOAD_DIR+str(userId))

        csv_file = DOWNLOAD_DIR+str(userId)+"/product_data.csv"

        # Define CSV fieldnames
        fieldnames = ['name', 'category', 'quantity', 'rate', 'orders']

        # Write JSON data to CSV file
        with open(csv_file, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

        return csv_file