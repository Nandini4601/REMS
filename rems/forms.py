from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, AnyOf
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from rems.models import Service, Employee, Apartment, House, Transaction, Types
from wtforms.fields.html5 import DateField


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('')


class EmployeeAddForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    DoB = DateField(validators=[DataRequired()])
    mobile = StringField('Mobile Number', validators=[DataRequired(), Length(min=7, max=10,
                                                                             message='Name length must be between %(min)d and %(max)d characters')])
    emer_mobile = StringField('Emergency mobile Number', validators=[DataRequired(), Length(min=7, max=10,
                                                                                            message='Name length must be between %(min)d and %(max)d characters')])
    email = StringField('Email Address', validators=[DataRequired(), Email(), Length(max=60)])
    service_list = QuerySelectField('Choose service', query_factory=lambda: Service.query, allow_blank=False,
                                    get_label='service_type')
    gender = StringField('Gender', validators=[DataRequired(), AnyOf(values=['Male', 'Female'],
                                                                     message='Gender must be male or female')])
    submit = SubmitField('Add Employee')

    def validate_email(self, email):
        emp = Employee.query.filter_by(email=email.data).first()
        if emp is not None:
            raise ValidationError('Please use a different email address.')


class HouseAddForm(FlaskForm):
    apt_num = QuerySelectField('Branch', query_factory=lambda: Apartment.query, allow_blank=False,
                               get_label='locality')
    house_num = StringField('House number', validators=[DataRequired()])
    bhk = StringField('BHK', validators=[DataRequired(),Length(max=2)])
    rent = StringField('Rent amount(in Thousands)', validators=[DataRequired(),Length(max=2,message='Enter amount in thousands')])
    advance = StringField('Advance amount(in Thousands)', validators=[DataRequired(),Length(max=2,message='Enter amount in thousands')])
    submit = SubmitField('Add House')


class TenantAddForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    DoB = DateField(validators=[DataRequired()])
    mobile = StringField('Mobile Number', validators=[DataRequired(), Length(min=7, max=10,
                                                                             message='Name length must be between %(min)d and %(max)d characters')])
    emer_mobile = StringField('Emergency mobile Number', validators=[DataRequired(), Length(min=7, max=10,
                                                                                            message='Name length must be between %(min)d and %(max)d characters')])
    email = StringField('Email Address', validators=[DataRequired(), Email(), Length(max=60)])
    spouse_mob = StringField('Spouse Mobile Number')
    apt_num = SelectField('Apartment', choices=['Theni', 'Madurai', 'Dindigul'], validate_choice=False)
    house_num = SelectField('House', validate_choice=False)
    submit = SubmitField('Add Tenant')


class TenantRemoveForm(FlaskForm):
    apt_num = SelectField('Apartment', choices=['Theni', 'Madurai', 'Dindigul'], render_kw={'class': 'form-control'},
                          validate_choice=False)
    house_num = SelectField('House', render_kw={'class': 'form-control'}, validate_choice=False)
    submit = SubmitField('Find Tenants')


class TransactionAddForm(FlaskForm):
    types_list = QuerySelectField('Choose type', query_factory=lambda: Types.query, allow_blank=False,
                                  get_label='transaction_type')
    Dot = DateField(validators=[DataRequired()], label='Date of Transaction')
    employee_list = QuerySelectField('Choose employee',
                                     query_factory=lambda: Employee.query.filter(
                                         Employee.service_id.in_((6, 7, 8))).all(),
                                     allow_blank=False,
                                     get_label='fname')
    apt_num = SelectField('Apartment', choices=['Theni', 'Madurai', 'Dindigul'], render_kw={'class': 'form-control'},
                          validate_choice=False)
    house_num = SelectField('House', render_kw={'class': 'form-control'}, validate_choice=False)
    tenant_id = SelectField('Tenants', render_kw={'class': 'form-control'}, validate_choice=False)
    amount = StringField('Amount', validators=[DataRequired(),Length(min=3)])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Add Transaction')
