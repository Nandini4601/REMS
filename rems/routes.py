from flask import render_template, flash, redirect, url_for, request, jsonify
from rems import app, db
from rems.forms import LoginForm, EmployeeAddForm, HouseAddForm, TenantAddForm
from flask_login import current_user, login_user, logout_user, login_required
from rems.models import User, Employee, House, Apartment, Tenant
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


@app.route('/addtenant', methods=['GET', 'POST'])
def add_tenant():
    form = TenantAddForm()
    form.house_num.choices = [(house.id, house.house_num) for house in House.query.all()]
    if form.validate_on_submit():
        tenant = Tenant(fname=form.firstname.data,
                        lname=form.lastname.data,
                        mob_num=form.mobile.data,
                        emer_num=form.emer_mobile.data,
                        email=form.email.data,
                        dob=form.DoB.data,
                        Spouse_num=form.spouse_mob.data,
                        house_id=form.house_num.data
                        )
        db.session.add(tenant)
        db.session.commit()
        flash('Successfully added new tenant')
        return redirect(url_for('home2'))
    return render_template('tenants.html', form=form)


@app.route('/addtenant/<area>')
def house(area):
    apt_num = Apartment.query.filter_by(locality=area).first().id
    houses = House.query.filter_by(apt_id=apt_num).all()

    houseArray = []

    for house in houses:
        houseObj = {}
        houseObj['id'] = house.id
        houseObj['house_num'] = house.house_num
        houseArray.append(houseObj)

    return jsonify({'houses': houseArray})


@app.route('/addtrans')
def add_trans():
    return render_template('transactions.html')

@app.route('/remtenant')
def rem_tenant():
    return render_template('tenants_rm.html')

@app.route('/rememployee')
def rem_employee():
    return render_template('rem_employee.html')

@app.route('/remhouses')
def rem_houses():
    return render_template('rem_houses.html')

@app.route('/list')
def list():
    return render_template('list.html')


@app.route('/addhouse', methods=['GET', 'POST'])
def add_house():
    form = HouseAddForm()
    if form.validate_on_submit():
        house = House(house_num=form.house_num.data,
                      bhk=form.bhk.data,
                      rent=form.rent.data,
                      advance=form.advance.data,
                      vacancy=False,
                      apt_id=form.apt_num.data.id,
                      )
        db.session.add(house)
        db.session.commit()
        flash('Successfully added new house')
        return redirect(url_for('home2'))
    return render_template('houses.html', form=form)


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
