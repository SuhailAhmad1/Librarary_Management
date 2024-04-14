from celery_app import celery
import time
from .mailing_service import sendEmail
from .csv_generation import generateCSV
from .scheduled_services import check_expirey, send_notice_if_not_login
from celery.schedules import crontab

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



celery.conf.beat_schedule = {
    'every-mid-night': {
        'task': 'app.services.jobs.check_for_expirey',
        'schedule': crontab(hour=0, minute=3),
    },
    'every-evening-night': {
        'task': 'app.services.jobs.check_for_last_login',
        'schedule': crontab(),
    }
}
# Define the task to be executed periodically
@celery.task
def check_for_expirey():
    print("Checking for user books exipery date...")
    if check_expirey():
        print('Successfully expired the books')
        return True
    print('Something went wrong..')
    return False

@celery.task
def check_for_last_login():
    print("Checking for user for last login...")
    if send_notice_if_not_login():
        print('Successfully sent notification to inacitve users')
        return True
    print('Something went wrong..')
    return False