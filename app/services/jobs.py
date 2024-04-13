from celery_app import celery
import time
from .mailing_service import sendEmail
from .csv_generation import generateCSV

@celery.task
def send_email_task(to, subject, message):
    print("Sending mail to : ", to)
    status = sendEmail(to, subject, message)
    if status:
        print("Successfully sent mail to : ", to)
        return True
    return False


@celery.task
def generate_csv(user_id):
    print("Generating CSV")
    # all_products = manager_service.get_all_products_db(user_id)
    all_products = generateCSV(user_id)
    print("Generation Done...")
    return all_products