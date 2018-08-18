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
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html', title='Home')

@flapp.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_admin:
        return render_template('dashboard.html', title='Dashboard')
    elif current_user.is_mentor:
        return redirect(url_for('mentee_list'))
    else:
        return redirect(url_for('mentor_list'))


@flapp.route('/mentor_list')
@login_required
def mentor_list():
    if current_user.is_admin:
        mentorList = Mentor.query.all()
        return render_template('mentorlist.html', title='Mentor List', mentors=mentorList)
    else:
        return render_template('404.html')

@flapp.route('/mentee_list')
@login_required
def mentee_list():
    if current_user.is_admin:
        menteeList = Mentee.query.all()
        return render_template('menteelist.html', title='Mentee List', mentees=menteeList)
    else:
        return render_template('404.html')

@flapp.route('/app_list')
@login_required
def app_list():
    if current_user.is_admin:
        appList = Application.query.all()
        return render_template('applist.html', title='Application List', apps=appList)
    else:
        return render_template('404.html')

@flapp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('dashboard')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@flapp.route('/register_user/<userType>', methods=['GET', 'POST'])
@login_required
def register_user(userType):
    if current_user.is_admin:
        try:
            userType = int(userType)
        except:
            return render_template('404.html')
        form = RegistrationForm()
        if (userType == 0):
            accessType = 0
        elif (userType == 1):
            accessType = 1
        else:
            accessType = 0
        if form.validate_on_submit():
            user = User(email=form.email.data, access=accessType)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Congratulations, you have registered user!')
            return redirect(url_for('login'))
        if accessType == 1:
            return render_template('register.html', title='Register Mentor', form=form)
        else:
            return render_template('register.html', title='Register Mentee', form=form)    
    else:
        return render_template('404.html')

@flapp.route('/del_app/<appId>')
@login_required
def del_app(appId):
    if current_user.is_admin:
        app = Application.query.filter_by(id=appId).first()
        db.session.delete(app)
        db.session.commit()
        # create User and Mentee accounts
        user = User(email=app.email, access=0)
        user.set_password(app.company)
        db.session.add(user)
        db.session.commit()
        mentee = Mentee(company=app.company, founder=app.founder, email=app.email, industry=app.industry, skills=app.skills, help_req=app.help_req)
        flash('You deleted the application for ' + app.company)
        return redirect(url_for('dashboard'))
    else:
        return render_template('404.html')

@flapp.route('/acc_app/<appId>')
@login_required
def acc_app(appId):
    if current_user.is_admin:
        app = Application.query.filter_by(id=appId).first()
        db.session.delete(app)
        app.accept = "Accepted"
        db.session.add(app)
        db.session.commit()
        flash('You accepted the application for ' + app.company)
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
        apply = Application(accept="Pending", company=form.company_name.data, founder=form.founder_names.data, email=form.contact_email.data, industry=form.industry.data, skills=form.team_skills.data, help_req=form.help_needed.data, interest=form.interest.data, gain=form.gain.data, stage=form.stage.data, relation=form.relation.data, web=form.website.data, links=form.business_docs.data)
        db.session.add(apply)
        db.session.commit()
        flash('Congratulations, you applied successfully!')
        return redirect(url_for('index'))
    elif request.method == 'GET':
        flash('Preload info.')
    return render_template('application.html', title='Mentee Application Form',
                           form=form)
