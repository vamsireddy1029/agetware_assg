from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import math
import uuid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db = SQLAlchemy(app)

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
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

@app.before_request
def create_tables_once():
    if not hasattr(app, 'db_initialized'):
        db.create_all()
        app.db_initialized = True


@app.route("/lend", methods=["POST"])
def lend():
    data = request.json
    cid = data["customer_id"]
    P = data["loan_amount"]
    N = data["loan_period"]
    R = data["interest_rate"]

    I = P * N * R / 100
    A = P + I
    months = N * 12
    EMI = A / months

    loan_id = str(uuid.uuid4())[:8]

    if not Customer.query.get(cid):
        db.session.add(Customer(id=cid))

    loan = Loan(
        id=loan_id,
        customer_id=cid,
        principal=P,
        interest=I,
        total_amount=A,
        emi_amount=EMI,
        loan_period_months=months
    )
    db.session.add(loan)

    txn = Transaction(loan_id=loan_id, type="LEND", amount=A)
    db.session.add(txn)
    db.session.commit()

    return jsonify({
        "loan_id": loan_id,
        "total_interest": I,
        "total_amount": A,
        "monthly_emi": EMI
    })

@app.route("/payment", methods=["POST"])
def payment():
    data = request.json
    lid = data["loan_id"]
    amount = data["amount"]
    pay_type = data["payment_type"]

    loan = Loan.query.get(lid)
    if not loan:
        return {"error": "Loan not found"}, 404

    loan.amount_paid += amount
    db.session.add(Transaction(loan_id=lid, type=pay_type, amount=amount))
    db.session.commit()

    balance = loan.total_amount - loan.amount_paid
    emis_left = math.ceil(balance / loan.emi_amount)

    return {
        "message": "Payment recorded successfully",
        "remaining_balance": balance,
        "emis_left": emis_left
    }

@app.route("/ledger/<loan_id>")
def ledger(loan_id):
    loan = Loan.query.get(loan_id)
    if not loan:
        return {"error": "Loan not found"}, 404

    txns = Transaction.query.filter_by(loan_id=loan_id).all()
    txn_list = [{"type": t.type, "amount": t.amount, "time": t.timestamp.isoformat()} for t in txns]

    balance = loan.total_amount - loan.amount_paid
    emis_left = math.ceil(balance / loan.emi_amount)

    return {
        "loan_id": loan_id,
        "transactions": txn_list,
        "balance_amount": balance,
        "monthly_emi": loan.emi_amount,
        "emis_left": emis_left
    }

@app.route("/account/<customer_id>")
def account(customer_id):
    loans = Loan.query.filter_by(customer_id=customer_id).all()
    result = []
    for loan in loans:
        balance = loan.total_amount - loan.amount_paid
        emis_left = math.ceil(balance / loan.emi_amount)
        result.append({
            "loan_id": loan.id,
            "principal": loan.principal,
            "total_interest": loan.interest,
            "total_amount": loan.total_amount,
            "emi_amount": loan.emi_amount,
            "amount_paid": loan.amount_paid,
            "emis_left": emis_left
        })

    return {"customer_id": customer_id, "loans": result}

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

