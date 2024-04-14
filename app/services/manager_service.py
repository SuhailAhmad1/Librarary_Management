from app.models.product import Product, Category, Order, UserRequest
from app.models.request import CategoryRequest
from app import db
import matplotlib.pyplot as plt
import os
import time
import json
import csv
from app.services.jobs import send_email_task
import pytz
from datetime import datetime, timedelta

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

    def convert_datetime(self, date_obj):

        date_obj += timedelta(hours=5, minutes=30)
        ist_date_str = date_obj.strftime("%I:%M %p - %d %b %Y")
        return ist_date_str


    def get_all_products_db(self, userid):
        manager_categories = Category.query.filter_by(
            user_id=userid, is_active=1).order_by(Category.id.desc())
        res = []
        for cat in manager_categories:
            this_cart = {
                "cat_id": cat.id,
                "cat_name": cat.name,
                "cat_description": cat.description,
                "created_at": self.convert_datetime(cat.created_at),
                "products": []
            }
            products = Product.query.filter_by(
                category_id=cat.id, is_active=1).order_by(Product.id.desc())
            for pro in products:
                this_pro = {
                    "id": pro.id,
                    "itemName": pro.name,
                    "author": pro.author,
                    "pdf_name": pro.book_path.split("/")[-1],
                }
                this_cart["products"].append(this_pro)
            res.append(this_cart)
        return res


    def upload(self, file, userid):
        current_time_stamp = str(time.time()).replace('.','')
        if not os.path.isdir(f"{DOWNLOAD_DIR}{userid}"):
            os.mkdir(f"{DOWNLOAD_DIR}{userid}")
        if not os.path.isdir(f"{DOWNLOAD_DIR}{userid}/{current_time_stamp}"):
            os.mkdir(f"{DOWNLOAD_DIR}{userid}/{current_time_stamp}")
        filepath = os.path.join(f"{DOWNLOAD_DIR}{userid}/{current_time_stamp}", file.filename)

        file.save(filepath)
        print(file)
        return filepath
    
    def add_product_db(self, userId, data, file):
        book_path = self.upload(file, userId)
        new_product = Product(
            name=data["book_name"],
            author=data["author"],
            book_path=book_path,
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
            product.author = data["author"]
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
    
    def get_book_path(self, product_id, userId):
        product = Product.query.filter_by(id=product_id, userid=userId).first()
        return product.book_path

    def get_man_user_requests_db(self, userId):
        all_reqs = UserRequest.query.order_by(UserRequest.id.desc()).all()

        res = []
        for request in all_reqs:
            this_order = {
                "id": request.id,
                "book_name": request.product.name,
                "author": request.product.author,
                "days_requested": request.days_requested,
                "user": request.user.email,
                "status": "Approved" if request.status == 1 else "Rejected" if request.status == -1 else "Pending"
            }
            res.append(this_order)
        return res

    def update_user_req_status_db(self, req_id, new_status):
        req = UserRequest.query.filter_by(id=req_id).first()
        if req:
            req.status = new_status
            if new_status == 1:
                req.approved_at = datetime.now()
            db.session.commit()
            new_status_word = "Approved" if new_status == 1 else "Rejected"
            send_email_task.delay(
                req.user.email,
                "Request status update",
                f"Your request has been {new_status_word}. Please check your dashboard for latest status"
            )
            return True
        return False

    def get_graph(self, userId):
        products = Product.query.filter_by(
            userid=userId).order_by(Product.id.desc())
        product_name = []
        product_count = []
        for pro in products:
            user_requests = UserRequest.query.filter_by(product_id=pro.id)
            count = 0
            for c in user_requests:
                count += 1
            this_product_name = pro.name
            cat = Category.query.filter_by(id=pro.category_id).first()
            this_product_name += "##" + (cat.name if cat else "del")
            product_name.append(this_product_name)
            product_count.append(count)
        plt.figure(figsize=(10, 6))
        plt.bar(product_name, product_count, color='skyblue')
        plt.xlabel('Books')
        plt.ylabel('Number of requests')
        plt.title('Books vs Number of Requests')
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
        fieldnames = ['book', 'author', 'book_pdf', 'category', 'number_of_requests']

        # Write JSON data to CSV file
        with open(csv_file, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

        return csv_file