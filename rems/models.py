from rems import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from rems import login


class Employee(db.Model):
    __tablename__ = 'employee'
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(25), index=True, unique=False)
    lname = db.Column(db.String(25), index=True, unique=False)
    mobile = db.Column(db.String(10), index=True, unique=True)
    emer_num = db.Column(db.String(10), index=False, unique=False)
    dob = db.Column(db.DateTime, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True)
    gender = db.Column(db.String(10), index=True, unique=False)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'))
    user = db.relationship("User", uselist=False, backref="employee")

    def __repr__(self):
        return '<Employee {}>   '.format(self.fname)


class Service(db.Model):
    __tablename__ = 'service'
    id = db.Column(db.Integer, primary_key=True)
    service_type = db.Column(db.String(25), unique=True)
    staff = db.relationship("Employee", uselist=False, backref="service")

    def __repr__(self):
        return '<Service {}>'.format(self.service_type)


class Apartment(db.Model):
    __tablename__ = 'apartment'
    id = db.Column(db.Integer, primary_key=True)
    apt_num = db.Column(db.String(5), index=True, unique=True)
    locality = db.Column(db.String(25), unique=False)
    house = db.relationship("House", uselist=False, backref="apartment")

    def __repr__(self):
        return '<Apartment {}>'.format(self.apt_num)


class House(db.Model):
    __tablename__ = 'house'
    id = db.Column(db.Integer, primary_key=True)
    house_num = db.Column(db.String(5), index=True, unique=False)
    bhk = db.Column(db.String(3), index=True, unique=False)
    rent = db.Column(db.String(4), index=True, unique=False)
    advance = db.Column(db.String(4), index=True, unique=False)
    vacancy = db.Column(db.Boolean, index=True, nullable=False, unique=False)
    apt_id = db.Column(db.Integer, db.ForeignKey('apartment.id'))
    tenant = db.relationship("Tenant", uselist=False, backref="house")

    def __repr__(self):
        return '<House {}>'.format(self.house_num)


class Tenant(db.Model):
    __tablename__ = 'tenant'
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(25), index=True, unique=False)
    lname = db.Column(db.String(25), index=True, unique=False)
    mob_num = db.Column(db.String(10), index=True, unique=True)
    emer_num = db.Column(db.String(10), index=True, unique=False)
    email = db.Column(db.String(120), index=False, unique=True)
    dob = db.Column(db.DateTime, nullable=False)
    Spouse_num = db.Column(db.String(10), unique=False, nullable=True)
    house_id = db.Column(db.Integer, db.ForeignKey('house.id'))

    def __repr__(self):
        return '<Tenant {}>'.format(self.fname)


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    emp_id = db.Column(db.Integer, db.ForeignKey('employee.id'))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
