# Banking Application -Python Flask

 > The objective of this project is to design simple APIs for a banking application.  
 
## Requirements

 - Python 3.x (or Python 2.x)
 - Virtual Environment
 - pip
 - Flask, SQLAlchemy

## Usage

 - Install either of the python versions (I used Python3)
 - Create new virtual environment using ``` python3 -m venv venv ```
 - Activate the virtual environment using ``` source venv/bin/activate ```
 - Install Flask using ``` pip install flask ```
 - Install SQLAlchemy, a SQL tool kit for python using ``` pip install SQLAlchemy ```
 - Run the application by running database file using ``` python database.py ``` and application file using ``` python app.py ``` respectively
 - Check the output by making POST and GET calls in Postman 

## Description of files

 - ***database.py***: Database file necessary to set up the banking app
 - ***app.py*** : Functionality to Open a new bank account, get account information, depositing and withdrawing from the account are written here
 
## References

 - [Setting up python flask application](http://www.patricksoftwareblog.com/steps-for-starting-a-new-flask-project-using-python3/)
 
Note: Implemented the app such that the account balance exists between ($100 < account value < $10m) all the time



 
 

