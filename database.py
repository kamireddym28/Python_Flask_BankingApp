from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy import Enum
import datetime
from sqlalchemy import DateTime

Base = declarative_base()

'''
User table to store user information
'''
class User(Base):
    __tablename__ = 'user'

    email = Column(String(250), primary_key=True)
    password = Column(String(250), nullable=False)

'''
Account table with account information of each user
'''
class Account(Base):
    __tablename__ = "account"

    account_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.email'))
    balance = Column(Integer)
    user = relationship(User)

'''
Transaction table to store transaction details of certain account
'''
class Transaction(Base):
    __tablename__ = 'transaction'

    transaction_id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey('account.account_id'))
    amount = Column(Integer)
    transaction_type = Column(Enum('deposit','Withdrawl'))
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    account = relationship(Account)

engine = create_engine('sqlite:///bankAccount.db')

Base.metadata.create_all(engine)
