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
	owner = db.Column(db.Integer(), db.ForeignKey('accounts.id'))
	name = db.Column(db.String(30), nullable=False)
	balance = db.Column(db.Integer, nullable=False)
	description = db.Column(db.String(100), nullable=False)
	 
	