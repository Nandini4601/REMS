from rems.models import Apartment, House, Tenant, Types, Employee, Service, Transaction
from rems import db
import datetime

''' this is for populating houses'''
# a = Apartment.query
# h = {
#      'Theni': [x.house_num for x in House.query.filter_by(apt_id=1).all()],
#      'Madurai': [x.house_num for x in House.query.filter_by(apt_id=2).all()],
#      'Dindigul': [x.house_num for x in House.query.filter_by(apt_id=3).all()],
#      }
#
# print(h)

'''To check services'''
# for s in Service.query:
#     print(s.id, s.service_type)

'''To verify foreign key in tenants'''
# t=Tenant.query
# print(t1.fname,t1.house_id)
# houses=set()
# for t in Tenant.query:
#      # db.session.delete(t)
#      # db.session.commit()
#      houses.add(t.house_id)
#      # h=House.query.filter_by(id=t.house_id).first()
#      # print(h.id,h.house_num,h.apt_id)
# houses=tuple(houses)

'''Obtaining vacant houses'''
# houses = House.query.filter(
#     House.id.not_in(map(lambda x: x[0], Tenant.query.with_entities(Tenant.house_id).all()))).all()
# list(map(lambda x: print(x.house_num, x.id), houses))

'''To obtain apartment localities as dictionaries'''
# ap = Apartment.query
# ids = map(lambda x: x.id, ap)
# locs = map(lambda x: x.locality, ap)
# loc = dict(zip(ids, locs))
# print(loc)

for house in House.query.filter_by(apt_id=2):
    print(house.id,house.house_num,house.rent,house.advance)

'''To populate the types db'''
# types = []
# types.append(Types(transaction_type='Rent'))
# types.append(Types(transaction_type='Electricity Bill'))
# types.append(Types(transaction_type='Maintenance'))
# types.append(Types(transaction_type='Plumbing'))
# types.append(Types(transaction_type='Painting'))
# types.append(Types(transaction_type='Other'))
# for type in types:
#     db.session.add(type)
# db.session.commit()

# for t in Types.query:
#     print(t)

'''Verifying Transactions'''
# trs=Transaction.query
# for t in trs:
#     print(t.desc,t.amt)


'''To verify employees '''
# emp = Employee.query
# for e in emp:
#     print(e.id, e.fname, e.service_id)
#     k = Service.query.filter_by(id=e.service_id).first()
#     print(k.id, k.service_type)
