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

if __name__ == '__main__':
	db.create_all()