from rems import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from rems import login


class Employee(db.Model):
    __tablename__ = 'employee'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), index=True, unique=False)
    mobile = db.Column(db.Integer, index=True, unique=True)
    user = db.relationship("User", uselist=False, backref="employee")

    def __repr__(self):
        return '<Employee {}>'.format(self.name)


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
