#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, MetaData, Table, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship

engine = sqlalchemy.create_engine('sqlite:///sqlitedb.db',echo = True)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)

    def __repr__(self):
        return "<id = %s User(name='%s', fullname='%s', password='%s')>" % (
                 self.id, self.name, self.fullname, self.password)

class Address(Base):
    __tablename__ = 'addresses'

    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="addresses")

    def __repr__(self):
        return "<Address(email_address='%s')>" % self.email_address

User.addresses = relationship('Address',order_by = Address.id , back_populates="user"
                              ,cascade = 'all,delete,delete-orphan')

Base.metadata.create_all(engine)

# session.add_all([User(name='ed', fullname='Ed Jones', password='edspassword'),
#                   User(name='wendy', fullname='Wendy Williams', password='foobar'),
#                   User(name='mary', fullname='Mary Contrary', password='xxg527'),
#                   User(name='fred', fullname='Fred Flinstone', password='blah')])

# jack = User(name='jack', fullname='Jack Bean', password='gjffdd')
#
# jack.addresses = [Address(email_address='jack@google.com'),
#                   Address(email_address='j25@yahoo.com')]
# session.add(jack)

# jake = session.query(User).filter(User.name=='jack').one()
# session.delete(jake)
# #
# session.commit()


for row in session.query(Address).all():
    print(row)