from app.models.product import Product, Category, Order, UserRequest
from app import db
from datetime import datetime, timedelta


class UserService:
    def get_all_items_db(self):
        all_categories = Category.query.filter_by(
            is_active=1).order_by(Category.id.desc())
        res = []
        for cat in all_categories:
            this_cart = {
                "cat_id": cat.id,
                "cat_name": cat.name,
                "seller": cat.user.email,
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

    def add_user_request_db(self, userId, data):
        req_item_count = UserRequest.query.filter_by(
            user_id=userId, status=0).count()
        if req_item_count >= 5:
            return False, "Max five new requests allowed"
        new_user_req = UserRequest(
            days_requested=data["no_of_days"],
            product_id=data["product_id"],
            user_id=userId,
            status=0
        )
        db.session.add(new_user_req)
        db.session.commit()
        return True, ""

    def get_user_requests_db(self, userId):

        req_items = UserRequest.query.filter_by(
            user_id=userId).order_by(UserRequest.id.desc())
        res = []
        for req_item in req_items:
            this_item = {
                "id": req_item.id,
                "status": "Approved" if req_item.status == 1 else "Rejected" if req_item.status == -1 else "Pending",
                "days_requested": req_item.days_requested
            }
            product = Product.query.filter_by(id=req_item.product_id).first()
            if product:
                this_item["book_name"] = product.name
                this_item["author"] = product.author
                res.append(this_item)
        return res

    def calculate_expirey(self, date_obj, days_requested):
        date_obj += timedelta(days=days_requested)
        return date_obj.strftime("%d %b %Y")

    def get_user_books_db(self, userId):
        books = UserRequest.query.filter_by(
            user_id=userId, status=1).order_by(UserRequest.id.desc())

        res = {
            "current": [],
            "completed": []
        }
        for book in books:
            this_book = {
                "id": book.id,
                "book_id": book.product.id,
                "book_name": book.product.name,
                "author": book.product.author,
                "days_requested": book.days_requested,
                "is_returned": book.is_returned,
                "expirey_at": self.calculate_expirey(book.approved_at, book.days_requested)
            }
            if not (book.is_returned or book.is_expired):
                res["current"].append(this_book)
            else:
                res["completed"].append(this_book)
        return res

    def get_book_path(self, product_id):
        product = Product.query.filter_by(id=product_id).first()
        return product.book_path

    def return_book_db(self, req_id, userId):
        request = UserRequest.query.filter_by(
            user_id=userId, id=req_id).first()
        if request:
            request.is_returned = 1
            db.session.commit()
            return True
        return False