from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, current_user, logout_user, login_required
from . import bcrypt, login_manager, mongo
from .models import User, Department, Title, EmployeeInfor

auth = Blueprint('auth', __name__)
main = Blueprint('main', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.get_user_by_id(int(user_id))

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.get_user_by_username(username)
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html')

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        User.add_user(username, password, role)
        flash('Your account has been created!', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@main.route('/')
@login_required
def home():
    return render_template('login.html')

@main.route('/assign_recipient')
@login_required
def assign_recipient():
    departments = Department.get_all_departments()
    employees = EmployeeInfor.get_all_employees()
    return render_template('phancongnguoinhan.html', departments=departments, employees=employees)

@main.route('/departmental_assignment')
@login_required
def departmental_assignment():
    departments = Department.get_all_departments()
    return render_template('phancongphongban.html', departments=departments)

@main.route('/receive_text')
@login_required
def receive_text():
    return render_template('tiepnhanvanbanden.html')

@main.route('/send_to_director')
@login_required
def send_to_director():
    titles = Title.get_all_titles()
    employees = EmployeeInfor.get_all_employees()
    return render_template('trinhgiamdoc.html', titles=titles, employees=employees)

@main.route('/text_consultant')
@login_required
def text_consultant():
    titles = Title.get_all_titles()
    employees = EmployeeInfor.get_all_employees()
    return render_template('thammuvanban.html', titles=titles, employees=employees)
@main.route('/data')
# @login_required
def show_data():
    data = mongo.db.con1.find_one()
    return render_template('data.html', data=data)