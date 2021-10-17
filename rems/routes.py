from flask import render_template, flash, redirect, url_for, request, jsonify
from rems import app, db
from rems.forms import LoginForm, EmployeeAddForm, HouseAddForm, TenantAddForm, TransactionAddForm, TenantRemoveForm
from flask_login import current_user, login_user, logout_user, login_required
from rems.models import User, Employee, House, Apartment, Tenant, Transaction, Service
from werkzeug.urls import url_parse


@app.route('/')
@app.route('/home')
def index():
    headings = ("BHK", "Locality", "Rent", "Advance", " ")
    ap = Apartment.query
    ids = map(lambda x: x.id, ap)
    places = map(lambda x: x.locality, ap)
    locs=dict(zip(ids,places))
    houses = House.query.filter(
        House.id.not_in(map(lambda x: x[0], Tenant.query.with_entities(Tenant.house_id).all()))).all()

    return render_template('homepage.html',headings=headings,houses=houses,apts=locs)


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
    form.house_num.choices = [(house.id, house.house_num) for house in House.query.filter_by(apt_id=1).all()]
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
        return redirect(url_for('home2'))
    return render_template('tenants.html', form=form)


@app.route('/remtenant', methods=['GET', 'POST'])
def rem_tenant():
    form = TenantRemoveForm()
    form.house_num.choices = [(house.id, house.house_num) for house in House.query.filter_by(apt_id=1).all()]
    if form.validate_on_submit():
        id = form.house_num.data
        headings = ("First Name", "Last Name", "mobile", "email", "DoB", "Spouse number ", " ")
        tens = Tenant.query.filter_by(house_id=id).all()
        return render_template('ten_rlist.html', headings=headings, data=tens)
    return render_template('tenants_rm.html', form=form)


@app.route('/remhouses', methods=['GET', 'POST'])
def rem_house():
    form = TenantRemoveForm()
    form.house_num.choices = [(house.id, house.house_num) for house in House.query.filter_by(apt_id=1).all()]
    if form.validate_on_submit():
        id = form.house_num.data
        return url_for('delete_house', id=id)
    return render_template('rem_house.html', form=form)


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


@app.route('/addtrans', methods=['GET', 'POST'])
def add_trans():
    form = TransactionAddForm()
    form.house_num.choices = [(house.id, house.house_num) for house in House.query.filter_by(apt_id=1).all()]
    form.tenant_id.choices = [(tenant.id, tenant.fname) for tenant in Tenant.query.filter_by(house_id=1).all()]
    if form.validate_on_submit():
        transaction = Transaction(type_id=form.types_list.data.id,
                                  dot=form.Dot.data,
                                  ten_id=form.tenant_id.data,
                                  emp_id=form.employee_list.data.id,
                                  amt=form.amount.data,
                                  desc=form.description.data
                                  )
        db.session.add(transaction)
        db.session.commit()
        return redirect(url_for('home2'))
    return render_template('transactions.html', form=form)


@app.route('/addtrans/<area>')
def house_trans(area):
    apt_num = Apartment.query.filter_by(locality=area).first().id
    houses = House.query.filter_by(apt_id=apt_num).all()

    houseArray = []

    for house in houses:
        houseObj = {}
        houseObj['id'] = house.id
        houseObj['house_num'] = house.house_num
        houseArray.append(houseObj)

    return jsonify({'houses': houseArray})


@app.route('/addtransh/<id>')
def tenant(id):
    tenants = Tenant.query.filter_by(house_id=id).all()

    tenantArray = []

    for tenant in tenants:
        tenantObj = {}
        tenantObj['id'] = tenant.id
        tenantObj['tenant_name'] = tenant.fname
        tenantArray.append(tenantObj)

    return jsonify({'tenants': tenantArray})


@app.route('/rememployee')
def rem_employee():
    services = Service.query
    return render_template('rem_employee.html', services=services)


@app.route('/rem_list/<int:id>')
def emp_list(id):
    headings = ("First Name", "Last Name", "mobile", "email", " ")
    emps = Employee.query.filter_by(service_id=id).all()
    return render_template('emp_rlist.html', headings=headings, data=emps)


@app.route('/delete_emp/<int:id>')
def delete_emp(id):
    emp_todel = Employee.query.filter_by(id=id).first()
    db.session.delete(emp_todel)
    db.session.commit()
    return render_template("ack2.html")


@app.route('/delete_ten/<int:id>')
def delete_ten(id):
    ten_todel = Tenant.query.filter_by(id=id).first()
    db.session.delete(ten_todel)
    db.session.commit()
    return render_template("ack2.html")


@app.route('/delete_house/<int:id>')
def delete_house(id):
    house_todel = House.query.filter_by(id=id).first()
    db.session.delete(house_todel)
    db.session.commit()
    return render_template("ack2.html")


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
        return redirect(url_for('home2'))
    return render_template('employee.html', form=form)
