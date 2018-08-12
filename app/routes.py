from app import flapp, db
from app.forms import LoginForm, RegistrationForm
from flask import render_template, flash, redirect, request, url_for
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Mentor
from werkzeug.urls import url_parse
import sys

@flapp.route('/')
@flapp.route('/index')
def index():
    return render_template('index.html', title='Home')

@flapp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', title='Dashboard')

@flapp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@flapp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@flapp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@flapp.route('/user/<id>')
@login_required
def user(id):
    user = User.query.filter_by(id=id)
    try:
        # check if user is defined
        user.id #maybe this should be user.id
    except AttributeError:
        print('USER NOT DEFINED', file=sys.stderr)
        # check if mentor is defined
        mentor = Mentor.query.filter_by(id=id)
        try:
            mentor.id #maybe this should be mentor.id
        except AttributeError:
            # return 404 if not mentor or user
            return render_template('404.html')
        else:
            is_mentor = True
            return render_template('user.html', user=mentor, is_mentor=is_mentor)
    else:
        is_mentor = False
        return render_template('user.html', user=user, is_mentor=is_mentor)
