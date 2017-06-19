import sys
#sqlalchemy configuration start same for every app

from sqlalchemy import Column,ForeignKey,Integer,String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base=declarative_base()



#configuration complete the above code is bascially required for every sqlalchemy app

class Restaurant(Base):
    __tablename__="restaurant"
    name=Column(String(100),nullable=False)
    id =Column(Integer,primary_key=True)

class MenuItem(Base):
    __tablename__="menu_item"
    name=Column(String(50),nullable=False)
    id=Column(Integer,primary_key=True)
    course=Column(String(100))
    description=Column(String(200))
    price=Column(String(8))

    # if table has any relationship than we declare here.
    restaurant = relationship(Restaurant)

    restaurant_id=Column(Integer,ForeignKey('restaurant.id'))


#initialize database and table

engine=create_engine('sqlite:///restaurantmenu.db')

Base.metadata.create_all(engine)