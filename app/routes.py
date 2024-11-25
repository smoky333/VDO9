from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, current_user, logout_user, login_required
from app import db, bcrypt
from app.models import User
from app.forms import RegistrationForm, LoginForm

routes = Blueprint('routes', __name__)


@routes.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('index.html')
    return redirect(url_for('routes.login'))


@routes.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('routes.index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Ваш аккаунт создан! Теперь вы можете войти.', 'success')
        return redirect(url_for('routes.login'))

    return render_template('register.html', form=form)


@routes.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('routes.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('routes.index'))
        else:
            flash('Не удалось войти. Проверьте имя пользователя и пароль.', 'danger')

    return render_template('login.html', form=form)


@routes.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('routes.login'))


@routes.route('/click', methods=['POST'])
@login_required
def click():
    current_user.clicks += 1
    db.session.commit()
    return redirect(url_for('routes.index'))
