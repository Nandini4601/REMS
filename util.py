from rems.models import Apartment, House, Tenant, Types
from rems import db

''' this is for populating houses'''
# a = Apartment.query
# h = {
#      'Theni': [x.house_num for x in House.query.filter_by(apt_id=1).all()],
#      'Madurai': [x.house_num for x in House.query.filter_by(apt_id=2).all()],
#      'Dindigul': [x.house_num for x in House.query.filter_by(apt_id=3).all()],
#      }
#
# print(h)


'''To verify foreign key in tenants'''
# t1=Tenant.query.first()
# print(t1.fname,t1.house_id)

# for t in Tenant.query:
#      # db.session.delete(t)
#      # db.session.commit()
#      print(t.fname, t.house_id)
#      h=House.query.filter_by(id=t.house_id).first()
#      print(h.id,h.house_num,h.apt_id)

'''To populate the types db'''
types = []
types.append(Types('Rent'))
types.append(Types('Electricity Bill'))
types.append(Types('Maintenance'))
types.append(Types('Plumbing'))
types.append(Types('Painting'))
types.append(Types('Other'))
for type in types:
    db.session.add(types)
db.session.commit()
