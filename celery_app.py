from celery import Celery
import os
from dotenv import load_dotenv
load_dotenv()


CELERY_BROKER_HOST = os.getenv("CELERY_BROKER_HOST")
CELERY_BROKER_PORT = os.getenv("CELERY_BROKER_PORT")
CELERY_BACKEND_HOST = os.getenv("CELERY_BACKEND_HOST")
CELERY_BACKEND_PORT = os.getenv("CELERY_BACKEND_PORT")

CELERY_BROKER = f"redis://{CELERY_BROKER_HOST}:{CELERY_BROKER_PORT}"
CELERY_BACKEND = f"redis://{CELERY_BACKEND_HOST}:{CELERY_BACKEND_PORT}"

celery = Celery(
    __name__,
    broker=CELERY_BROKER,
    backend=CELERY_BACKEND
)

celery.conf.imports = [
    'app.services.jobs',
]
