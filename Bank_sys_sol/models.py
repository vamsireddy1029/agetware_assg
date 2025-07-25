from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Customer(db.Model):
    id = db.Column(db.String, primary_key=True)

class Loan(db.Model):
    id = db.Column(db.String, primary_key=True)
    customer_id = db.Column(db.String, db.ForeignKey('customer.id'))
    principal = db.Column(db.Float)
    interest = db.Column(db.Float)
    total_amount = db.Column(db.Float)
    emi_amount = db.Column(db.Float)
    loan_period_months = db.Column(db.Integer)
    amount_paid = db.Column(db.Float, default=0)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    loan_id = db.Column(db.String, db.ForeignKey('loan.id'))
    type = db.Column(db.String)
    amount = db.Column(db.Float)
    timestamp = db.Column(db.DateTime)
