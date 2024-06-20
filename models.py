from database import Base
from sqlalchemy import Column,Integer,String,Boolean,Text,ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType


class User(Base):
    __tablename__ ='user'
    id = Column(Integer,primary_key=True)
    user =Column(String(25),unique=True)
    email = Column(String(80),unique=True)
    password =Column(Text,nullable=True)
    is_staff = Column(Boolean,default=False) 
    Orders =relationship('order',back_populates='user')


    def __repr__(self):
        return f"<User{self.username}"
    
class Order(Base):
    ORDER_STATUSES = (
        ('PENDING','pending'),
        ('IN-TRANSIT','in-transit'),
        ('DELIEVERED','delievered')
    )

    PIZZA_SIZES = (
        ('SMALL','small'),
        ('MEDIUM','medium'),
        ('LARGE','large'),
        ('EXTRA-LARGE','extra-large'),
    )


    __tablename__='orders'
    id =Column(Integer,primary_key=True)
    quantity =Column(Integer,nullable=False)
    order_status =Column(ChoiceType(ORDER_STATUSES),default="PENDING")
    pizza_sizer =Column(ChoiceType(PIZZA_SIZES),default="SMALL")
    user_id =Column(Integer,ForeignKey('user.id'))
    user =relationship('User',back_populates='orders')

    def __repr__(self):
        return f"<Order {self.id}"
