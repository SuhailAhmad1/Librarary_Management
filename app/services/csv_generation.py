from app.models.product import Product, Category, UserRequest
from app import create_app
import csv
import os
import time
app = create_app()

DOWNLOAD_DIR = os.getenv("DOWNLOAD_DIR")


def generateCSV(userId):
    with app.app_context():
        products = Product.query.filter_by().order_by(Product.id.desc())
        product_info = []
        for pro in products:
            this_pro = {
                "book": pro.name,
                "author": pro.author,
                "book_pdf": pro.book_path.split("/")[-1],
                "category": Category.query.filter_by(id=pro.category_id).first().name,
                "number_of_requests": UserRequest.query.filter_by(product_id=pro.id).count(),
            }

            product_info.append(this_pro)
        time.sleep(4)
        
        return product_info
