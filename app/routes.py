from app import flapp, db
from app.forms import MenteeMatchForm, MentorSelectForm, LoginForm, ResetPasswordRequestForm, ResetPasswordForm, MentorRegistrationForm, MenteeRegistrationForm, EditMenteeProfileForm, ApplicationForm, EditMentorProfileForm, EditCohortProfileForm, AdminRegistrationForm
from flask import render_template, flash, redirect, request, url_for
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Mentor, Mentee, Application, Company
from werkzeug.urls import url_parse
import sys
from app.email import send_password_reset_email, accept_applicant, match_mentee

@flapp.route('/')
@flapp.route('/index')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    return render_template('index.html', title='Home')

@flapp.route('/cohort_faq')
@login_required
def cohort_faq():
    if current_user.is_company():
        return render_template('faq.html', title='FAQ')
    else:
        return render_template('404.html')

@flapp.route('/homepage')
@login_required
def homepage():
    if current_user.is_admin():
        return render_template('home_mentor.html', title='Home')
    elif current_user.is_mentor():
        return render_template('home_mentor.html', title='Home')
    elif current_user.is_company():
        return render_template('home_cohort.html', title='Home')
    else:
        return render_template('home_gm.html', title='Home')


@flapp.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_admin():
        return render_template('dashboard.html', title='Dashboard')
    elif current_user.is_mentor():
        return redirect(url_for('mentee_list'))
    else:
        return redirect(url_for('mentor_list'))

@flapp.route('/shortlist')
@login_required
def shortlist():
    if current_user.is_company():
        return redirect(url_for('mentor_shortlist'))
    elif current_user.is_admin():
        flash('Feature not available for admin.')
        return redirect(url_for('dashboard'))
    elif current_user.is_mentor():
        return redirect(url_for('mentee_shortlist'))
    else:
        return redirect(url_for('mentor_shortlist'))

@flapp.route('/mentor_list')
@login_required
def mentor_list():
    mentorList = Mentor.query.all()
    cohort = None
    mentee = None
    for mentor in mentorList:
        user = User.query.filter_by(email=mentor.email).first()
        # clean the data a bit before passing to mentees
        if current_user.access == 0:
            mentor.email = None
        mentor.email_hash = user.email_hash
        mentor.mentees = []
        for m in mentor.users:
            mentee = Mentee.query.filter_by(email=m.email).first()
            mentor.mentees.append(mentee)
    if current_user.is_company():
        cohort = Company.query.filter_by(email=current_user.email).first()
    elif current_user.is_admin():
        print('no data to grab')
    elif current_user.is_mentor():
        print('no data to grab')
    else:
        mentee = Mentee.query.filter_by(email=current_user.email).first()        
    return render_template('mentorlist.html', title='Mentor List', mentors=mentorList, menteeInfo=mentee, cohortInfo=cohort)

@flapp.route('/del_mentorpref/<mentorId>')
@login_required
def del_mentorpref(mentorId):
    user = User.query.filter_by(email_hash=mentorId).first()
    mentor = Mentor.query.filter_by(email=user.email).first()
    if current_user.is_company():
        cohort = Company.query.filter_by(email=current_user.email).first()
        mentor.cohort = None
        db.session.commit()
        flash('Removed from shortlist.')
    elif current_user.is_admin():
        flash('Feature not available.')
    elif current_user.is_mentor():
        flash('Removed from shortlist.')
    else:
        mentee = Mentee.query.filter_by(email=current_user.email).first()
        mentor.mentee = None
        db.session.commit()
        flash('Shortlist has been updated.')
    return redirect(url_for('mentor_list'))

@flapp.route('/acc_mentorpref/<mentorId>')
@login_required
def acc_mentorpref(mentorId):
    user = User.query.filter_by(email_hash=mentorId).first()
    mentor = Mentor.query.filter_by(email=user.email).first()
    if current_user.is_company():
        cohort = Company.query.filter_by(email=current_user.email).first()
        mentor.cohort = cohort
        db.session.commit()
        flash('Shortlist has been updated.')
    elif current_user.is_admin():
        flash('Feature not available.')
    elif current_user.is_mentor():
        flash('Feature not available.')
    else:
        mentee = Mentee.query.filter_by(email=current_user.email).first()
        mentor.mentee = mentee
        db.session.commit()
        flash('Shortlist has been updated.')
    return redirect(url_for('mentor_list'))

@flapp.route('/del_menteepref/<menteeId>')
@login_required
def del_menteepref(menteeId):
    user = User.query.filter_by(email_hash=menteeId).first()
    if current_user.is_mentor():
        mentor = User.query.filter_by(email=current_user.email).first()
        if user.is_company():
            cohort = Company.query.filter_by(email=user.email).first()
            cohort.mentorpref = None
        else:
            mentee = Mentee.query.filter_by(email=user.email).first()
            mentee.mentorpref = None
        db.session.commit()
        flash('Removed from shortlist.')
    else:
        flash('Feature not available.')
    return redirect(url_for('mentee_list'))

@flapp.route('/acc_menteepref/<menteeId>')
@login_required
def acc_menteepref(menteeId):
    user = User.query.filter_by(email_hash=menteeId).first()
    print('1', user)
    if current_user.is_mentor():
        mentor = User.query.filter_by(email=current_user.email).first()
        if user.is_company():
            cohort = Company.query.filter_by(email=user.email).first()
            print('2', mentor)
            cohort.mentorpref = mentor
            print('3', cohort)
            print('4', cohort.mentorpref)
        else:
            mentee = Mentee.query.filter_by(email=user.email).first()
            mentee.mentorpref = mentor
        db.session.commit()
        flash('Shortlist has been updated.')
    else:
        flash('Feature not available.')
    return redirect(url_for('mentee_list'))

@flapp.route('/mentor_shortlist')
@login_required
def mentor_shortlist():
    if current_user.is_company():
        cohort = Company.query.filter_by(email=current_user.email).first()
        mentorList = Mentor.query.filter_by(cohort=cohort)
    elif current_user.is_admin():
        mentorList = None
    elif current_user.is_mentor():
        mentorList = None
    else:
        mentee = Mentee.query.filter_by(email=current_user.email).first()
        mentorList = Mentor.query.filter_by(mentee=mentee)
    for mentor in mentorList:
        user = User.query.filter_by(email=mentor.email).first()
        # clean the data a bit before passing to mentees
        if current_user.access == 0:
            mentor.email = None
        mentor.email_hash = user.email_hash
            
    return render_template('mentorshortlist.html', title='Mentor Shortlist', mentors=mentorList)

@flapp.route('/mentee_shortlist')
@login_required
def mentee_shortlist():
    if current_user.is_mentor():
        user = User.query.filter_by(email=current_user.email).first()
        menteeList = Mentee.query.filter_by(mentorpref=user)
        cohortList = Company.query.filter_by(mentorpref=user)

        for mentee in menteeList:
            user = User.query.filter_by(email=mentee.email).first()
            mentee.email_hash = user.email_hash
        
        for cohort in cohortList:
            user = User.query.filter_by(email=cohort.email).first()
            cohort.email_hash = user.email_hash
    else:
        menteeList = None
        cohortList = None            
    return render_template('menteeshortlist.html', title='Mentee Shortlist', mentees=menteeList, cohorts=cohortList)


@flapp.route('/combined_list')
@login_required
def combined_list():          
    menteeList = Mentee.query.all()
    companyList = Company.query.all()
    for mentee in menteeList:
        user = User.query.filter_by(email=mentee.email).first()
        mentee.email_hash = user.email_hash
        mentee.mentor = user.mentor
        #if mentor remove empty accts
        if current_user.is_mentor():
            if mentee.company is None:
                menteeList.remove(mentee)
    for company in companyList:
        user = User.query.filter_by(email=company.email).first()
        company.email_hash = user.email_hash
        company.mentor = user.mentor
        #if mentor remove empty accts
        if current_user.is_mentor():
            if company.company is None:
                companyList.remove(company)
    mentor = None
    if current_user.is_mentor():
        mentor = User.query.filter_by(email=current_user.email).first()
    return render_template('combinedlist.html', title='Mentee List', mentees=menteeList, cohorts=companyList, mentor=mentor)

@flapp.route('/company_list')
@login_required
def company_list():          
    companyList = Company.query.all()
    for company in companyList:
        user = User.query.filter_by(email=company.email).first()
        company.email_hash = user.email_hash
        company.mentor = user.mentor
        #if mentor remove empty accts
        if current_user.is_mentor():
            if company.company is None:
                companyList.remove(company)
    mentor = None
    if current_user.is_mentor():
        mentor = User.query.filter_by(email=current_user.email).first()
    return render_template('companylist.html', title='Mentee List', cohorts=companyList, mentor=mentor)

@flapp.route('/mentee_list')
@login_required
def mentee_list():          
    menteeList = Mentee.query.all()
    for mentee in menteeList:
        user = User.query.filter_by(email=mentee.email).first()
        mentee.email_hash = user.email_hash
        mentee.mentor = user.mentor
        #if mentor remove empty accts
        if current_user.is_mentor():
            if mentee.company is None:
                menteeList.remove(mentee)
    mentor = None
    if current_user.is_mentor():
        mentor = User.query.filter_by(email=current_user.email).first()
    return render_template('menteelist.html', title='Mentee List', mentees=menteeList, mentor=mentor)

@flapp.route('/app_list')
@login_required
def app_list():
    if current_user.is_admin():
        appList = Application.query.all()
        return render_template('applist.html', title='Application List', apps=appList)
    else:
        return render_template('404.html')

@flapp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('homepage')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@flapp.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    form = MenteeRegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, access=0)
        user.set_password(form.password.data)
        user.set_id()
        db.session.add(user)
        db.session.commit()
        mentee = Mentee(email=form.email.data)
        db.session.add(mentee)
        db.session.commit()
        flash('Congratulations, you have registered ' + form.email.data)
        return redirect(url_for('login'))
    return render_template('signup.html', title='Sign Up', form=form)    

@flapp.route('/register_user/<userType>', methods=['GET', 'POST'])
@login_required
def register_user(userType):
    if current_user.is_admin():
        try:
            userType = int(userType)
        except:
            return render_template('404.html')
        if (userType == 0):
            form = MenteeRegistrationForm()
            accessType = 0
        elif (userType == 1):
            form = MentorRegistrationForm()
            accessType = 1
        elif (userType == 3):
            # NEED A COHORT REGISTRATION FORM
            form = AdminRegistrationForm()
            accessType = 3
        else:
            form = AdminRegistrationForm()
            accessType = 0
        if form.validate_on_submit():
            user = User(email=form.email.data, access=accessType)
            user.set_password(form.password.data)
            user.set_id()
            db.session.add(user)
            db.session.commit()
            # create mentor
            if accessType == 1:
                mentor = Mentor(first_name=form.first_name.data,
                                last_name=form.last_name.data,
                                email=form.email.data,
                                headline=form.headline.data,
                                about_me=form.about.data,
                                avail=form.avail.data,
                                skills=form.skills.data,
                                industry=dict(form.industry.choices).get(form.industry.data),
                                mentor_company=form.company.data,
                                position=form.position.data,
                                university=dict(form.university.choices).get(form.university.data),
                                major=dict(form.major.choices).get(form.major.data),
                                grad_year=form.grad_year.data,
                                linkedin=form.linkedin.data,
                                twitter=form.twitter.data)
                db.session.add(mentor)
                db.session.commit()
            else:
                mentee = Mentee(first_name=form.first_name.data,
                                last_name=form.last_name.data,
                                email=form.email.data,
                                headline=form.headline.data,
                                about=form.about.data,
                                skills=form.skills.data,
                                university=dict(form.university.choices).get(form.university.data),
                                major=dict(form.major.choices).get(form.major.data),
                                year=dict(form.year.choices).get(form.year.data),
                                company=form.company.data,
                                industry=dict(form.industry.choices).get(form.industry.data),
                                linkedin=form.linkedin.data,
                                twitter=form.twitter.data)
                # ADD CODE HERE TO CREATE A COMPANY ACCOUNT AND LINK IT TO THIS ACCOUNT IF ACCESSTYPE == 3
                db.session.add(mentee)
                db.session.commit()
            flash('Congratulations, you have registered ' + form.email.data)
            return redirect(url_for('login'))
        if accessType == 1:
            return render_template('register_mentor.html', title='Register Mentor', form=form)
        elif accessType == 3:
            return render_template('register_mentee.html', title='Register Company', form=form)
        else:
            return render_template('register_mentee.html', title='Register Mentee', form=form)    
    else:
        return render_template('404.html')

@flapp.route('/del_app/<appId>')
@login_required
def del_app(appId):
    if current_user.is_admin():
        app = Application.query.filter_by(id=appId).first()
        db.session.delete(app)
        db.session.commit()
        flash('You deleted the application for ' + app.company)
        return redirect(url_for('dashboard'))
    else:
        return render_template('404.html')

@flapp.route('/acc_app/<appId>')
@login_required
def acc_app(appId):
    if current_user.is_admin():
        app = Application.query.filter_by(id=appId).first()
        app.accept = "Accepted"
        db.session.commit()
        # applying with a mentee account, only requires the creation of a company acct
        # create User and Mentee accounts
        #user = User(email=app.email, access=0)
        #user.set_password(app.company)
        #user.set_id()
        #db.session.add(user)
        #db.session.commit()

        # turn all members into cohort accounts
        email_array = []
        if app.email is not None:
            email_array = app.email.split(", ")
        company = Company(company=app.company,
                        members=app.founder,
                        email=app.email,
                        industry=app.industry,
                        help_req=app.help_req)
        db.session.add(company)
        # links members listed via email to company

        for mem_email in email_array:
            
            user = User.query.filter_by(email=mem_email).first()
            # make acct a company having acct
            user.access = 3
            mentee = Mentee.query.filter_by(email=mem_email).first()
            # link acct to company
            mentee.company_l = company

        db.session.commit()
        flash('You accepted the application for ' + app.company)
        accept_applicant(user, app)
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
    user = User.query.filter_by(email_hash=userId).first()
    try:
        # check if user is defined
        user.id
    except AttributeError:
        return render_template('404.html')
    mentees = []
    skill_array = []
    if user == current_user:
        if current_user.is_admin():
            return render_template('404.html')
        elif current_user.is_mentor():
            info = Mentor.query.filter_by(email=user.email).first()
            if info.skills is not None:
                skill_array = info.skills.split(", ")
            for m in info.users:
                mentee = Mentee.query.filter_by(email=m.email).first()
                mentees.append(mentee)
        else:
            info = Mentee.query.filter_by(email=user.email).first()
            if info.skills is not None:
                skill_array = info.skills.split(", ")

    elif current_user.is_admin():
        if user.is_admin():
            # dont load profile for
            return render_template('404.html')
        elif user.is_mentor():
            info = Mentor.query.filter_by(email=user.email).first()
            if info.skills is not None:
                skill_array = info.skill.split(", ")
        else:
            info = Mentee.query.filter_by(email=user.email).first()
            if info.skills is not None:
                skill_array = info.skills.split(", ")
            
    elif current_user.is_mentor():
        if user.is_admin():
            return render_template('404.html')
        elif user.is_mentor():
            return render_template('404.html')
        else:
            # current user = mentor, can only view mentees
            info = Mentee.query.filter_by(email=user.email).first()
            if info.skills is not None:
                skill_array = info.skills.split(", ")
    else:
        if user.is_admin():
            return render_template('404.html')
        elif user.is_mentor():
            # current user = mentee, can only view mentors
            info = Mentor.query.filter_by(email=user.email).first()
            if info.skills is not None:
                skill_array = info.skill.split(", ")
            # clean the data a bit before passing to mentees
            info.email = None
            user.email = None
        else:
            return render_template('404.html')
    
    return render_template('user.html', title='Profile', user=user, info=info, mentor=user.mentor, mentees=mentees, skill_array=skill_array)

@flapp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if current_user.is_admin():
        return render_template('404.html')
    elif current_user.is_mentor():
        form = EditMentorProfileForm(current_user.email)
        info = Mentor.query.filter_by(email=current_user.email).first()
        if form.validate_on_submit():
            current_user.email = form.email.data
            current_user.set_id()
            info.first_name = form.first_name.data
            info.last_name = form.last_name.data
            info.email = form.email.data
            info.about_me = form.about.data
            info.headline = form.headline.data
            info.avail = form.avail.data
            info.skill = form.skill.data
            info.mentor_company = form.company.data
            info.position = form.position.data
            info.industry = dict(form.industry.choices).get(form.industry.data)
            info.university = dict(form.university.choices).get(form.university.data)
            info.major = dict(form.major.choices).get(form.major.data)
            info.grad_year = form.grad_year.data
            info.linkedin = form.linkedin.data
            info.twitter = form.twitter.data
            db.session.commit()
            flash('Your changes have been saved.')
            return redirect(url_for('user', userId=current_user.email_hash))
        elif request.method == 'GET':
            form.first_name.data = info.first_name
            form.last_name.data = info.last_name
            form.email.data = current_user.email
            form.headline.data = info.headline
            form.about.data = info.about_me
            form.avail.data = info.avail
            form.skill.data = info.skills
            form.company.data = info.mentor_company
            form.position.data = info.position
            form.industry.data = info.industry
            form.university.data = info.university
            form.major.data = info.major
            form.grad_year.data = info.grad_year
            form.linkedin.data = info.linkedin
            form.twitter.data = info.twitter
        return render_template('edit_profile.html', title='Edit Profile', form=form)
    elif current_user.is_company():
        form = EditCohortProfileForm(current_user.email)
        info = Company.query.filter_by(email=current_user.email).first()

        if form.validate_on_submit():
            current_user.email = form.email.data
            current_user.set_id()
            info.email = form.email.data
            info.company = form.company_name.data
            info.members = form.member_names.data
            info.industry = dict(form.industry.choices).get(form.industry.data)
            info.help_req = form.help_needed.data
            db.session.commit()
            flash('Your changes have been saved.')
            return redirect(url_for('user', userId=current_user.email_hash))
        elif request.method == 'GET':
            form.email.data = current_user.email
            form.company_name.data = info.company
            form.member_names.data = info.members
            form.industry.data = info.industry
            form.university.data = info.university
            form.major.data = info.major
            form.grad_year.data = info.grad_year
            form.help_needed.data = info.help_req
        return render_template('edit_profile.html', title='Edit Profile', form=form)
    else:
        form = EditMenteeProfileForm(current_user.email)
        info = Mentee.query.filter_by(email=current_user.email).first()
        
        if form.validate_on_submit():
            # current_user.email = form.email.data
            current_user.set_id()
            info.first_name = form.first_name.data
            info.last_name = form.last_name.data
            info.headline = form.headline.data
            info.about = form.about.data
            info.company = form.company.data
            info.university = dict(form.university.choices).get(form.university.data)
            info.major = dict(form.major.choices).get(form.major.data)
            info.year = dict(form.year.choices).get(form.year.data)
            info.industry = dict(form.industry.choices).get(form.industry.data)
            info.email = form.email.data
            info.skills = form.skill.data
            info.linkedin = form.linkedin.data
            info.twitter = form.twitter.data
            db.session.commit()
            flash('Your changes have been saved.')
            return redirect(url_for('user', userId=current_user.email_hash))
        elif request.method == 'GET':
            form.first_name.data = info.first_name
            form.last_name.data = info.last_name
            form.headline.data = info.headline
            form.about.data = info.about
            form.university.data = info.university
            form.major.data = info.major
            form.year.data = info.year
            form.email.data = current_user.email
            form.company.data = info.company
            form.industry.data = info.industry
            form.skill.data = info.skills
            form.linkedin.data = info.linkedin
            form.twitter.data = info.twitter
        return render_template('edit_profile.html', title='Edit Profile', form=form)


@flapp.route('/application', methods=['GET', 'POST'])
@login_required
def application():
    form = ApplicationForm()
    if form.validate_on_submit():
        form_emails = form.team_emails.data
        # make sure to store the email of the user submitting it, so when accepted can change their acct and link them
        if current_user.email not in form_emails:
            form_emails = form_emails + ', ' + current_user.email
        apply = Application(accept="Pending",
                            company=form.company_name.data,
                            founder=form.founder_names.data,
                            email=form_emails,
                            industry=form.industry.data,
                            skills=form.team_skills.data,
                            help_req=form.help_needed.data,
                            interest=form.interest.data,
                            gain=form.gain.data,
                            stage=form.stage.data,
                            relation=form.relation.data,
                            web=form.website.data,
                            links=form.business_docs.data)
        db.session.add(apply)
        db.session.commit()
        flash('Congratulations, you applied successfully!')
        return redirect(url_for('index'))
    return render_template('application.html', title='Cohort Application Form',
                           form=form)

@flapp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset.html', title='Reset Password', form=form)

@flapp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    else:
        user = User.verify_reset_password_token(token)
        if not user:
            return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        else:
            return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)

@flapp.route('/reset_password', methods=['GET', 'POST'])
def reset_pw():
    if current_user.is_authenticated:
        user = current_user
    else:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('dashboard'))
    return render_template('reset_password.html', form=form)

@flapp.route('/update_mentor', methods=['GET', 'POST'])
@login_required
def update_mentor():      
    mentee = Mentee.query.filter_by(email=current_user.email).first()
    if mentee is None:
         return redirect(url_for('dashboard'))   
    form = MentorSelectForm()
    if form.validate_on_submit():
        mentee.mentor1 = form.mentor1.data
        mentee.mentor2 = form.mentor2.data
        mentee.mentor3 = form.mentor3.data
        db.session.commit()
        flash('Your mentor preferences have been updated.')
        return redirect(url_for('dashboard'))
    elif request.method == 'GET':
        form.mentor1.data = mentee.mentor1
        form.mentor2.data = mentee.mentor2
        form.mentor3.data = mentee.mentor3
    return render_template('mentorprefs.html', title='Mentor Preferences', form=form)

@flapp.route('/add_mentor/<menteeId>', methods=['GET', 'POST'])
@login_required
def add_mentor(menteeId):
    if current_user.is_admin():
        mentee = Mentee.query.filter_by(id=menteeId).first()
        user = User.query.filter_by(email=mentee.email).first()
        form = MenteeMatchForm()
        if form.validate_on_submit():
            mentorId = form.mentor.data
            mentor = Mentor.query.filter_by(id=mentorId).first()
            user.mentor = mentor
            db.session.commit()
            flash(mentee.company + ' mentor has been updated.')
            match_mentee(user, mentee)
            return redirect(url_for('dashboard'))
        elif request.method == 'GET':
            if user.mentor:
                form.mentor.data = user.mentor.id
        return render_template('menteematch.html', title='Update Mentor', form=form, mentee=mentee)
    else:
        return render_template('404.html')

@flapp.route('/privacy')
def privacy():
    return render_template('privacy.html', title='Privacy Policy')

@flapp.route('/terms')
def terms():
    return render_template('terms.html', title='Terms of Service')

@flapp.route('/contact')
def contact():
    return render_template('contact.html', title='Contact')