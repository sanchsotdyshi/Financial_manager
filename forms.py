from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Email, Length,  EqualTo, InputRequired


class RegistrationForm(FlaskForm):
	name = StringField("Придумайте никнейм: ", validators=[DataRequired(), Length(min=6, max=15)])
	email = StringField("Введите почту: ", validators=[Email(message='Некоректный имейл')])
	password = PasswordField('Придумайте пароль', [InputRequired(), EqualTo('confirm', message='Пароли должны совпадать')])
	confirm = PasswordField('Подтвердите пароль', [InputRequired(), EqualTo('password', message='Пароли должны совпадать')])
	submit = SubmitField("Зарегистрироваться")

class LoginForm(FlaskForm):
	name = StringField("Введите никнейм: ", validators=[DataRequired(), Length(min=6, max=15)])
	password = PasswordField('Введите пароль пароль', [InputRequired(),])
	submit = SubmitField("Войти")

class CreateWalletForm(FlaskForm):
	name = StringField("Название:", validators=[DataRequired(), Length(min=0, max=30)])
	description = StringField("Описание:", validators=[ Length(min=0, max=100)])
	submit = SubmitField("Создать")
