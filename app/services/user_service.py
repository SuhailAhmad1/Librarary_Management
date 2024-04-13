from app.models.product import Product, Category, UserCart, Order
from app import db


class UserService:
    def get_all_items_db(self):
        all_categories = Category.query.filter_by(is_active=1).order_by(Category.id.desc())
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
                    "rate": pro.rate,
                    "quantity": pro.quantity,
                }
                this_cart["products"].append(this_pro)
            res.append(this_cart)
        return res

    def add_cart_db(self, userId, data):
        new_cart = UserCart(
            quantity=data["quantity"],
            amount=data["amount"],
            rate=data["rate"],
            product_id=data["product_id"],
            notes=data["notes"],
            user_id=userId
        )
        db.session.add(new_cart)
        db.session.commit()
        return True

    def get_cart_db(self, userId):
        cart_items = UserCart.query.filter_by(
            user_id=userId).order_by(UserCart.id.desc())
        res = []
        for cart_item in cart_items:
            this_item = {
                "cart_id": cart_item.id,
                "quantity": cart_item.quantity,
                "rate": cart_item.rate,
                "amount": cart_item.amount,
                "notes": cart_item.notes,
                "product_id": cart_item.product_id
            }
            product = Product.query.filter_by(id=cart_item.product_id).first()
            if product:
                this_item["product_name"] = product.name
                this_item["quantity_available"] = product.quantity
                res.append(this_item)
        return res

    def edit_cart_db(self, userId, data):
        cart_item = UserCart.query.filter_by(
            id=data["cart_id"], user_id=userId).first()
        if cart_item:
            cart_item.amount = data["amount"]
            cart_item.quantity = data["quantity"]
            db.session.commit()
            return True
        else:
            return False

    def delete_cart_db(self, userId, cartId):
        cart_item = UserCart.query.filter_by(id=cartId, user_id=userId).first()
        if cart_item:
            db.session.delete(cart_item)
            db.session.commit()
            return True
        return False

    def place_order_db(self, userId, data):
        all_cart_details = UserCart.query.filter_by(user_id=userId)
        user_email = all_cart_details[0].user.email
        for cart_details in all_cart_details:
            new_order = Order(
                user_id=userId,
                product_id=cart_details.product_id,
                status="Placed",
                address=data["address"],
                quantity=cart_details.quantity,
                amount=cart_details.amount,
                rate=cart_details.rate,
                notes=cart_details.notes,
                full_name=data["full_name"],
                phone_number=data["phone_number"]
            )
            db.session.add(new_order)

            # Updating product Quantity
            product = Product.query.filter_by(
                id=cart_details.product_id).first()
            if product:
                product.quantity = product.quantity - cart_details.quantity

            # Deleting the cart item
            db.session.delete(cart_details)

        db.session.commit()
        return True, user_email

    def get_user_orders_db(self, userId):
        orders = Order.query.filter_by(
            user_id=userId).order_by(Order.id.desc())

        res = []
        for order in orders:
            this_order = {
                "id": order.id,
                "product_name": order.product.name,
                "amount": order.amount,
                "address": order.address,
                "status": order.status
            }
            res.append(this_order)
        return res
