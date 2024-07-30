from flask_login import UserMixin
from . import mongo, bcrypt


class User(UserMixin):
    def __init__(self, id_user, username, password, role):
        self.id = id_user
        self.username = username
        self.password = password
        self.role = role

    @staticmethod
    def get_user_by_username(username):
        user_data = mongo.db.users.find_one({"Signin.username": username}, {"Signin.$": 1})
        if user_data and "Signin" in user_data:
            user_info = user_data["Signin"][0]
            return User(user_info['id_user'], user_info['username'], user_info['password'], user_info['role'])
        return None

    @staticmethod
    def add_user(username, password, role):
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = {
            "id_user": mongo.db.users.find_one(sort=[("Signin.id_user", -1)])["Signin"][-1]["id_user"] + 1,
            "username": username,
            "password": hashed_password,
            "role": role
        }
        mongo.db.users.update_one({}, {'$push': {"Signin": new_user}})
        return new_user

    @staticmethod
    def get_all_users():
        users = mongo.db.users.find_one({}, {"Signin": 1})
        return users.get("Signin", [])

    @staticmethod
    def get_user_by_id(user_id):
        user_data = mongo.db.users.find_one({"Signin.id_user": user_id}, {"Signin.$": 1})
        if user_data and "Signin" in user_data:
            return user_data["Signin"][0]
        return None

class Department:
    @staticmethod
    def get_all_departments():
        departments = mongo.db.users.find_one({}, {"Departments": 1})
        return departments.get("Departments", [])

class Title:
    @staticmethod
    def get_all_titles():
        titles = mongo.db.users.find_one({}, {"Title": 1})
        return titles.get("Title", [])

class EmployeeInfor:
    @staticmethod
    def get_all_employees():
        employees = mongo.db.users.find_one({}, {"EmployeeInfor": 1})
        return employees.get("EmployeeInfor", [])
