
# Library Management - Backend Branch

Backend for library management 


## Features

This repo contains All APIs (Rest) and Backend jobs



## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

- `SECRET_KEY = 'you-will-never-guess'`
- `JWT_SECRET_KEY = 'you-will-never-guess'`
- `SQLITE_URL = "sqlite:///grocery_db.sqlite3"`
- `DOWNLOAD_DIR = "path/to/your/folder/"`
- `APP_EMAIL = "your email to send out emails"`
- `PASS_KEY = "your email app password"`
- `CELERY_BROKER_HOST = "localhost"`
- `CELERY_BROKER_PORT = "6379/0"`
- `CELERY_BACKEND_HOST = "localhost"`
- `CELERY_BACKEND_PORT = "6379/1"`




## Installation Backend

Steps to start the Python server :
- Needs Python v3.10+
- Clone the repo : 
```https://github.com/SuhailAhmad1/Librarary_Management```
- Change the working dir : 
```cd Librarary_Management```
- Checkout to the main branch:
 ```git checkout backend```
- Create a virtual environment :
```python3 -m venv .venv```
- Activate the environment :
```source .venv/bin/activate```
- Install all the required dependencies : 
```pip install -r requirements```
- Run the server using :
```python run.py```
- Your server will be up and running at "http://127.0.0.1:5000"

## Installation Celery
- After Backend is up, Few more steps to start celery server
- Open another terminal tab :
`cd "path/to/Librarary_Management"`
- Again activate the environment :
```source .venv/bin/activate```
- Run the below command : 
```celery -A celery_app worker --loglevel=INFO -c 2 -B```
- I am keeping the concurrency level to 2 workers, you can change it based on your system. Now your backend server as well as celery are up and running


## Tech Stack


- Python, Flask, SQL-Alchemy, Celery, Redis, SMTP, JinJa2, JWT, Cron
