from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Transaction, Base, Account, User
import time
import random, string, json

app = Flask(__name__)

engine = create_engine('sqlite:///bankAccount.db?check_same_thread=False')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

'''
Function to 'GET' information about certain account along with transaction details
'''
@app.route('/getDetails', methods = ['GET'])
def get():
    email_id = request.args['email']
    print(email_id)
    acc = session.query(Account).filter(Account.user_id == email_id)
    returnObj = {}
    count = acc.count()
    if count == 1 :
        acc_id = acc.one().account_id
        bal = acc.one().balance
        trans = session.query(Transaction).filter(Transaction.account_id == acc_id)
        rows = trans.statement.execute().fetchall()
        trans_details = []
        for row in rows:
             trans_details.append({"transaction_id" : row.transaction_id, "type" : row.transaction_type, "amount" : row.amount, "timestamp" : row.timestamp})
        returnObj = {"status" : "Success. Please find the account transaction details", "account_details" : {"account_id" : acc_id, "balance" : bal}, "transaction_details": trans_details}
    else:
        returnObj = {"status" : "Fail. Account information not found", "account_details" : {}}
    return jsonify(returnObj)

'''
Function to 'deposit' amount into account when balance is below $10m and update the account balance
'''
@app.route('/deposit', methods = ['POST'])
def deposit():
    email_id = request.json['email']
    amt = request.json['amt']
    acc = session.query(Account).filter(Account.user_id == email_id)
    count = acc.count()
    balance = 0
    acc_id = ""
    returnObj = {"status":"Failed. Transaction can't be made at this time. Please try again"}
    if count == 1:
        balance = acc.one().balance
        acc_id = acc.one().account_id
    if acc_id != "" and amt > 0:
        if balance + amt < 10000000:
            trans = Transaction(transaction_id=str(round(time.time()))+"".join(random.choices(string.digits, k=6)), account_id = acc_id, amount = amt, transaction_type = "deposit")
            session.add(trans)
            session.commit()
            session.query(Account).filter(Account.account_id == acc_id).update({"balance": balance + amt}, synchronize_session='evaluate')
            session.commit()
            returnObj = {"status":"Successfully deposited the amount"}
        else:
            returnObj = {"status":"Transaction unsuccessful. Balance exceeds $10million"}
    else:
        returnObj = {"status" : "Failed. Account unavailable or Deposit amount is negative or zero. Expected positive value"}
    return jsonify(returnObj)

'''
Function to 'withdraw' amount from account when balance is above $100 and update the account balance
'''
@app.route('/withdraw', methods = ['POST'])
def withdraw():
    email_id = request.json['email']
    amt = request.json['amt']
    acc = session.query(Account).filter(Account.user_id == email_id)
    count = acc.count()
    balance = 0
    acc_id = ""
    returnObj = {"status":"Failed. Transaction can't be made at this time. Please try again"}
    if count == 1:
        balance = acc.one().balance
        acc_id = acc.one().account_id
    if acc_id != "" and amt > 0:
        if balance - amt > 100:
            trans = Transaction(transaction_id=str(round(time.time()))+"".join(random.choices(string.digits, k=6)), account_id = acc_id, amount = amt, transaction_type = "Withdrawl")
            session.add(trans)
            session.commit()
            session.query(Account).filter(Account.account_id == acc_id).update({"balance": balance - amt}, synchronize_session='evaluate')
            session.commit()
            returnObj = {"status":"Successfully withdrew the amount"}
        else:
            returnObj = {"status":"Transaction unsuccessful. Balance is less than $100"}
    else:
        returnObj = {"status" : "Failed. Account unavailable or withdraw amount is negative or zero. Expected positive value"}
    return jsonify(returnObj)

'''
Function to make 'POST' request to open an account for every new user
'''
@app.route('/OpenAccount', methods = ['POST'])
def post():
    email_id = request.json['email']
    findUser = session.query(User).filter(User.email==email_id)
    x = "fail"
    count = findUser.count()
    if count == 0:
        new_User = User(email=email_id, password=''.join(random.choices(string.ascii_letters + string.digits, k=8)))
        session.add(new_User)
        session.commit()
        x = "success"
    else:
        print(findUser.one().email)
        print(findUser.one().password)
        x = "exists"
    if x == 'success':
        acc = Account(account_id = str(round(time.time()))+"".join(random.choices(string.digits, k=8)), user_id=email_id, balance=100)
        session.add(acc)
        print(acc.account_id)
        session.commit()
        return jsonify({"status": "Successfully opened a new account"})
    else:
        return jsonify({"status":"User already exists"})

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.run(debug=True)
    app.run(host='0.0.0.0', port=5000)
