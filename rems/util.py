from rems.models import Apartment,House
''' this is for populating houses'''
a=Apartment.query
h=House.query
for house in h:
    print(house.id,house.apt_id,house.house_num,house.advance)

