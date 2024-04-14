from app.models.product import Product, Category, UserRequest
from app.models.user import User
from app import create_app, db
from datetime import datetime, timedelta
import os
from app.services.mailing_service import sendEmail, sendEmailReport
app = create_app()

DOWNLOAD_DIR = os.getenv("DOWNLOAD_DIR")


def check_expirey():
    with app.app_context():
        user_requests = UserRequest.query.filter(
            UserRequest.approved_at.isnot(None)
        ).order_by(UserRequest.id.desc())
        for book in user_requests:
            book_expirey_date = book.approved_at + \
                timedelta(days=book.days_requested)
            current_date = datetime.now().date()
            if current_date >= book_expirey_date.date():
                book.is_expired = 1
                db.session.commit()
    return True


def send_notice_if_not_login():
    with app.app_context():
        users = User.query.filter_by(
            role="user").order_by(User.id.desc())

        for user in users:
            current_date = datetime.now().date()
            if user.last_login.date() != current_date:
                sendEmail(user.email, "New Books",
                          "Why do not you check our latest collection of books")
                print(user.email)
    return True

def send_reports():
    with app.app_context():
        users = User.query.filter_by(
            role="user").order_by(User.id.desc())
        
        for user in users:
            report_data = []
            user_books = UserRequest.query.filter_by(
            user_id=user.id).order_by(UserRequest.id.desc())
            for book in user_books:
                this_book = {
                    "book_name": book.product.name,
                    "author": book.product.author,
                    "section": book.product.category.name,
                    "status": "Approved" if book.status == 1 else "Rejected" if book.status == -1 else "Pending",
                    "days_requested": book.days_requested,
                    "is_returned": book.is_returned
                }
                report_data.append(this_book)
            sendEmailReport(user.email, "Monthly report", report_data)
    return True