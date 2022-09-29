from flask import Flask, request, render_template, make_response, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

from forms import RegistrationForm, LoginForm, CreateWalletForm
from models import  db, Account, Wallet

app = Flask('Financial_manager')

app.config['SECRET_KEY'] = 'a really really really really long secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://flask_root:443011asd@localhost:5432/financial_manager_db'

# Инициализация БД
db.init_app(app)


# Функция отображения для регистрации
@app.route('/registration/', methods=['GET', 'POST'])
def registration():
	# Словарь для передачи переменных в шаблон 
	context = dict()
	
	form = RegistrationForm()

	if form.validate_on_submit():
		# Если данные из формы прошли валидацию,
		new_acc = Account(username=form.name.data, email=form.email.data, password=form.password.data)
		db.session.add(new_acc)
		db.session.commit()

	context['form'] = form
	return render_template('registration.html', **context)


# Функция отображения для входа
@app.route('/login/', methods=['GET', 'POST'])
def login():
	# Словарь для передачи переменных в шаблон 
	context = dict()
	
	if request.cookies.get('login'):
		return redirect(url_for('main_page'))

	form = LoginForm()
	if form.validate_on_submit():
		name = form.name.data
		password = form.password.data
		result = db.session.query(Account).filter(Account.username == name, Account.password == password)
		if result.first():
			res = redirect(url_for('main_page'))
			res.set_cookie('login', 'yes', max_age=60*60*24*7)
			res.set_cookie('name', name, max_age=60*60*24*7)
			res.set_cookie('password', password, max_age=60*60*24*7)
			return res
			print('Аккаунт существует')
		else:
			print('Аккаунт не существует')

	context['form'] = form
	return render_template('login.html', **context)

#Функция чтобы разлогиниться
@app.route('/logout/', methods=['GET', 'POST'])
def logout():
	res = redirect(url_for('login'))
	res.set_cookie('login', '', max_age=0)
	res.set_cookie('name', '', max_age=0)
	res.set_cookie('password', '', max_age=0)
	return res


@app.route('/', methods=['GET', 'POST'])
def default():
	return redirect(url_for('main_page'))

#Функция оттображения главной страницы
@app.route('/main_page/', methods=['GET', 'POST'])
def main_page():
	context = dict()
	form = CreateWalletForm()
	context['form'] = form
	if request.cookies.get('login'):
		context['name'] = request.cookies.get('name')
		user = db.session.query(Account).filter(Account.username==request.cookies.get('name')).first()
		context['wallets'] = db.session.query(Wallet).filter(Wallet.owner==user.id)
	else:
		return redirect(url_for('login'))

	return render_template('main_page.html', **context)

@app.route('/create_wallet/', methods=['GET', 'POST'])
def create_wallet():
	form = CreateWalletForm()
	print(form.name.data)
	print(form.description.data)

	user = db.session.query(Account).filter(Account.username==request.cookies.get('name')).first()
	new_wallet = Wallet(name=form.name.data, owner=user.id, balance=0, description=form.description.data)
	db.session.add(new_wallet)
	db.session.commit()
	return redirect(url_for('main_page'))


if __name__ == "__main__":
	#создаем контекс приложения, что бы создать таблицы
	with app.app_context():
		db.create_all()
	app.run(debug=True)