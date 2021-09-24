from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from rems.models import Service


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('')


class EmployeeAddForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    DoB = DateField(validators=[DataRequired()])
    mobile = StringField('Mobile Number', validators=[DataRequired()])
    emer_mobile = StringField('Emergency mobile Number', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired()])
    service_list = QuerySelectField('Choose service', query_factory=lambda: Service.query, allow_blank=False)
    gender = StringField('Gender', validators=[DataRequired()])
    submit = SubmitField('')
