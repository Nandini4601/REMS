from rems import app, db
from rems.models import User, Employee,Service,Tenant,House,Apartment


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Employee': Employee,'Service': Service, 'Tenant' : Tenant, 'House' : House, 'Apartment' : Apartment}


if __name__ == '__main__':
    app.run(debug=True)
