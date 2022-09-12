from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

from forms import RegistrationForm
from models import  db, Account

app = Flask('Financial_manager')

app.config['SECRET_KEY'] = 'a really really really really long secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://flask_root:443011asd@localhost/financial_manager_db'


db.init_app(app)

@app.route('/sign_up/', methods=['GET', 'POST'])
def sing_up():
	context = dict()
	
	form = RegistrationForm()
	if form.validate_on_submit():
		new_acc = Account(username=form.name.data, email=form.email.data, password=form.password.data)
		db.session.add(new_acc)
		db.session.commit()

		print(form.name.data)
		print(form.email.data)
		print(form.password.data)

	context['form'] = form
	return render_template('sign_up.html', **context)


if __name__ == "__main__":
    app.run(debug=True)