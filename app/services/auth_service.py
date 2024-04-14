from app.models.user import User
from app import db
import traceback
from passlib.hash import pbkdf2_sha256 as sha256
from datetime import datetime

class AuthService:
    def get_user_by_email(self, email):
        try:
            user = User.query.filter_by(email=email).first()
            if user:
                return {
                    "email": user.email,
                    "username": user.username,
                    "password": user.password,
                    "id": user.id,
                    "user_role": user.role
                }
            else:
                return {}
        except Exception as e:
            print(traceback.print_exc(e))
            return False

    def create_new_user(self, data):
        try:
            data["password"] = sha256.hash(data["password"])
            new_user = User(data["email"], data["password"])
            db.session.add(new_user)
            db.session.commit()
            return True
        except Exception as e:
            print(traceback.print_exc(e))
            return False

    def get_all_users(self):
        users = User.query.all()
        return [user.username for user in users]

    def update_last_login(self, userId):
        user = User.query.filter_by(id=userId).first()
        user.last_login = datetime.now()
        db.session.commit()

    def check_if_manager(self, userId):
        user = User.query.filter_by(id=userId).first()
        if user.role in ["librarian", "admin"]:
            return True
        return False

    def check_if_admin(self, userId):
        user = User.query.filter_by(id=userId).first()
        if user.role == "admin":
            return True
        return False
