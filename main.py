from flask import Flask, request, render_template, make_response, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

from forms import RegistrationForm, LoginForm, CreateWalletForm, CreateCategoryForm, CreateTransactionForm, CreateReportForm
from models import  db, Account, Wallet, Category, Transaction

app = Flask('Financial_manager')

app.config['SECRET_KEY'] = 'a really really really really long secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://flask_root:443011asd@localhost:5432/financial_manager_db'

# Связываем БД с приложением
db.init_app(app)


# Функция отображения для регистрации
@app.route('/registration/', methods=['GET', 'POST'])
def registration():
	# Словарь для передачи переменных в шаблон 
	context = dict()
	
	form = RegistrationForm()

	if form.validate_on_submit():
		# Если данные из формы прошли валидацию...
		# Проверяем нет ли аккаунта с таким именем или почтой
		find_ac_name = None
		find_ac_email = None
		find_ac_name = db.session.query(Account).filter(Account.username==form.name.data)
		find_ac_email = db.session.query(Account).filter(Account.email==form.email.data)
		if find_ac_name.first() != None or find_ac_email.first() != None:
			# Если такое имя или почту уже успользуют выводим соответствующую ошибку
			if find_ac_name.first() != None:
				context['name_error'] = True
			if find_ac_email.first() != None:
				context['email_error'] = True
		else:
			# Если нет аккаунта с таким данными, то создаем и выводим сообщение об успешном создании
			new_acc = Account(username=form.name.data, email=form.email.data, password=form.password.data)
			db.session.add(new_acc)
			db.session.commit()
			context['reg_success'] = True


	context['form'] = form
	return render_template('registration.html', **context)


# Функция отображения для входа
@app.route('/login/', methods=['GET', 'POST'])
def login():
	context = dict()
	if request.cookies.get('login'):
		return redirect(url_for('main_page'))

	form = LoginForm()
	if form.validate_on_submit():
		name = form.name.data
		password = form.password.data
		result = db.session.query(Account).filter(Account.username == name, Account.password == password)
		account = result.first()
		if account:
			res = redirect(url_for('main_page'))
			res.set_cookie('login', 'yes', max_age=60*60*24*7)
			res.set_cookie('id', str(account.id), max_age=60*60*24*7)
			res.set_cookie('name', name, max_age=60*60*24*7)
			res.set_cookie('password', password, max_age=60*60*24*7)
			return res

		else:
			context['error'] = True

	context['form'] = form
	return render_template('login.html', **context)

#Функция чтобы разлогиниться
@app.route('/logout/', methods=['GET', 'POST'])
def logout():
	#Стираем все данные из куки
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

# Фунция создает новый счет
@app.route('/create_wallet/', methods=['POST'])
def create_wallet():
	form = CreateWalletForm()
	user = db.session.query(Account).filter(Account.username==request.cookies.get('name')).first()
	new_wallet = Wallet(name=form.name.data, owner=user.id, balance=0, description=form.description.data)
	db.session.add(new_wallet)
	db.session.commit()
	return redirect(url_for('main_page'))

# Функция для этображения счета
@app.route('/wallet/<int:wallet_id>', methods=['GET', 'POST'])
def wallet(wallet_id):
	if request.cookies.get('login'):
		wallet = db.session.query(Wallet).filter(Wallet.id==wallet_id).first()
		if wallet.owner != int(request.cookies.get('id')):
			return redirect(url_for('main_page'))
		
		context = dict() 
		context['wallet'] = wallet
		context['wallet_id'] = wallet_id
		transactions = db.session.query(Transaction).order_by(Transaction.date.desc()).filter(Transaction.wallet==wallet_id)
		context['transactions'] = transactions
		form = CreateTransactionForm() 
		form.wallet_id.data = wallet_id
		categories_list = []  
		categories = db.session.query(Category)
		for category in categories:
			categories_list.append((str(category.id), category.name))

		form.category.choices=categories_list

		context['form'] = form
		return render_template('wallet.html', **context)
	
	return redirect(url_for('login'))

#Создание новой записи в кошельке
@app.route('/create_transaction/<int:wallet_id>', methods=['GET', 'POST'])
def create_transaction(wallet_id):
	form = CreateTransactionForm()
	wallet = db.session.query(Wallet).filter(Wallet.id==wallet_id).first()
	transaction_category = db.session.query(Category).filter(Category.id==form.category.data).first()
	new_transaction = Transaction(wallet=wallet_id, category=form.category.data, category_name=transaction_category.name, value=form.value.data, date=form.date.data, description=form.description.data)
	db.session.add(new_transaction)
	if transaction_category.income:
		wallet.balance = wallet.balance + form.value.data

	else:
		wallet.balance = wallet.balance - form.value.data

	db.session.add(wallet)
	db.session.commit()
	return redirect(url_for('wallet', wallet_id=wallet_id))

# Функция отбражения настроек
@app.route('/settings/', methods=['GET', 'POST'])
def settings():
	form = CreateCategoryForm()
	context = {
		'form':form
	}
	return render_template('settings.html', **context)

#Функция создания категорий
@app.route('/create_category/', methods=['GET', 'POST'])
def create_category():
	form = CreateCategoryForm()

	if form.validate_on_submit():
		name = form.name.data
		income = form.income.data
		new_category = Category(name=name, income=income)
		db.session.add(new_category)
		db.session.commit()

	table = db.session.query(Category)
	for cat in table:
		print('{} {}'.format(cat.name, cat.income))

	return redirect(url_for('settings'))

#Отчеты
@app.route('/reports/<int:wallet_id>', methods=['GET', 'POST'])
def reports(wallet_id):
	context = {}
	form = CreateReportForm()
	context['form'] = form
	context['wallet_id'] = wallet_id
	report_table = []
	report_transactions = db.session.query(Transaction).filter(Transaction.wallet==wallet_id, Transaction.date>=form.start_date.data, Transaction.date<=form.finish_date.data)
	if form.validate_on_submit():
		
		for category in db.session.query(Category).all():
			sum_ = 0
			transactions = report_transactions.filter(Transaction.category==category.id)
			for transaction in transactions:
				sum_ += transaction.value

			report_table.append((category.name, sum_))

		context['transactions'] = report_transactions
		context['report_table'] = report_table
	return render_template('reports.html', **context)


if __name__ == "__main__":
	#создаем контекс приложения, что бы создать таблицы
	with app.app_context():
		db.create_all()
	app.run(debug=True)