from app import flapp, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, ApplicationForm
from flask import render_template, flash, redirect, request, url_for
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Mentor, Mentee, Application
from werkzeug.urls import url_parse
import sys

@flapp.route('/')
@flapp.route('/index')
def index():
    return render_template('index.html', title='Home')

@flapp.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_admin:
        appList = Application.query.all()
        return render_template('dashboard.html', title='Dashboard', apps=appList)
    return render_template('dashboard.html', title='Dashboard')

@flapp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@flapp.route('/register_user', methods=['GET', 'POST'])
@login_required
def register_user():
    if current_user.is_admin:
        form = RegistrationForm()
        if form.validate_on_submit():
            user = User(email=form.email.data, access=0)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('login'))
        return render_template('register.html', title='Register', form=form)
    else:
        return render_template('404.html')

@flapp.route('/del_app/<appId>')
@login_required
def del_app(appId):
    if current_user.is_admin:
        app = Application.query.filter_by(id=appId).first()
        db.session.delete(app)
        db.session.commit()
        flash('You deleted the application for ', str(app.company))
        return redirect(url_for('dashboard'))
    else:
        return render_template('404.html')

@flapp.route('/acc_app/<appId>')
@login_required
def acc_app(appId):
    if current_user.is_admin:
        app = Application.query.filter_by(id=appId).first()
        db.session.delete(app)
        app.accept = True
        db.session.add(app)
        db.session.commit()
        flash('You accepted the application for ', str(app.company))
        return redirect(url_for('dashboard'))
    else:
        return render_template('404.html')

@flapp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@flapp.route('/user/<userId>')
@login_required
def user(userId):
    user = User.query.filter_by(id=userId).first()
    try:
        # check if user is defined
        user.id
    except AttributeError:
        # check if mentor is defined
        mentor = Mentor.query.filter_by(id=userId)
        try:
            mentor.id
        except AttributeError:
            print('USER NOT DEFINED', file=sys.stderr)
            # return 404 if not mentor or user
            return render_template('404.html')
        else:
            is_mentor = True
            return render_template('user.html', user=mentor, is_mentor=is_mentor)
    else:
        is_mentor = False
        return render_template('user.html', user=user, is_mentor=is_mentor)

@flapp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.first_name = form.first_name.data
        current_user.last_name = form.first_name.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)

@flapp.route('/application', methods=['GET', 'POST'])
def application():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ApplicationForm()
    if form.validate_on_submit():
        apply = Application(accept=False, company=form.company_name.data, founder=form.founder_names.data, email=form.contact_email.data, industry=form.industry.data, skills=form.team_skills.data, help_req=form.help_needed.data, interest=form.interest.data, gain=form.gain.data, stage=form.stage.data, relation=form.relation.data, web=form.website.data, links=form.business_docs.data)
        db.session.add(apply)
        db.session.commit()
        flash('Congratulations, you applied successfully!')
        return redirect(url_for('index'))
    elif request.method == 'GET':
        flash('Preload info.')
    return render_template('application.html', title='Mentee Application Form',
                           form=form)
