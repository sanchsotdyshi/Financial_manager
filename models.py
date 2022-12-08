from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class Account(db.Model):
	__tablename__ = 'accounts'

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(30), nullable=False)
	email = db.Column(db.String(30), nullable=False)
	password = db.Column(db.String(30), nullable=False)

	# Позже сделаю подтверждение эмейла пока по дефолту True
	email_verification = db.Column(db.Boolean(), nullable=False, default=True)

	wallets = db.relationship('Wallet', backref='account')

class Wallet(db.Model):
	__tablename__ = 'wallets'

	id = db.Column(db.Integer, primary_key=True)
	owner = db.Column(db.Integer, db.ForeignKey('accounts.id'))
	name = db.Column(db.String(30), nullable=False)
	balance = db.Column(db.Integer, nullable=False)
	description = db.Column(db.String(100), nullable=False)

class Category(db.Model):
	__tablename__ = 'categories'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(30), nullable=False)
	income = db.Column(db.Boolean(), nullable=False, default=False)

class Transaction(db.Model):
	__tablename__ = 'transactions'

	id = db.Column(db.Integer, primary_key=True)
	wallet = db.Column(db.Integer, db.ForeignKey('wallets.id'))
	category = db.Column(db.Integer, db.ForeignKey('categories.id'))
	category_name = db.Column(db.String(30), default='None')
	value =  db.Column(db.Float,nullable=False)
	date = db.Column(db.Date, nullable=False)
	description = db.Column(db.String(100), nullable=False)

	 
	