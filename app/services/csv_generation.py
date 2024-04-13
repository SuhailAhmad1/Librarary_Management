from app.models.product import Product, Category, Order
from app import create_app
import csv
import os
import time
app = create_app()

DOWNLOAD_DIR = os.getenv("DOWNLOAD_DIR")


def generateCSV(userId):
    with app.app_context():
        products = Product.query.filter_by(
            userid=userId).order_by(Product.id.desc())
        product_info = []
        for pro in products:
            this_pro = {
                "name": pro.name,
                "category": Category.query.filter_by(id=pro.category_id).first().name,
                "rate": pro.rate,
                "quantity": pro.quantity,
                "orders": Order.query.filter_by(product_id=pro.id).count()
            }

            product_info.append(this_pro)
        time.sleep(4)
        
        return product_info
