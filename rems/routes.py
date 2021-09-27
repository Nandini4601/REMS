from flask import render_template, flash, redirect, url_for, request, g
from rems import app, db
from rems.forms import LoginForm, EmployeeAddForm
from flask_login import current_user, login_user, logout_user, login_required
from rems.models import User, Employee
from werkzeug.urls import url_parse



@app.route('/')
@app.route('/home')
def index():
    return render_template('homepage.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home2'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home2')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/home2')
@login_required
def home2():
    return render_template('index.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/addtenant')
def add_tenant():
    return render_template('tenants.html')

@app.route('/addtrans')
def add_trans():
    return render_template('transactions.html')

@app.route('/addhouse')
def add_house():
    return render_template('houses.html')


@app.route('/addemp', methods=['GET', 'POST'])
def add_employee():
    form = EmployeeAddForm()
    if form.validate_on_submit():
        emp = Employee(fname=form.firstname.data,
                       lname=form.lastname.data,
                       mobile=form.mobile.data,
                       emer_num=form.emer_mobile.data,
                       dob=form.DoB.data,
                       email=form.email.data,
                       gender=form.gender.data,
                       service_id=form.service_list.data.id)
        db.session.add(emp)
        db.session.commit()
        flash('Successfully added new employee')
        return redirect(url_for('home2'))
    return render_template('employee.html', form=form)
