from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User, Application, Mentor

schoolList = [('dal', 'Dalhousie University'),
              ('mcg', 'McGill University'),
              ('mac', 'McMaster University'),
              ('qu', "Queen's University"),
              ('ru', 'Ryerson University'),
              ('sfu', 'Simon Fraser University'),
              ('ubc', 'University of British Columbia'),
              ('ug', 'University of Guelph'),
              ('uoft', 'University of Toronto'),
              ('uw', 'University of Waterloo'),
              ('uwo', 'University of Western Ontario'),
              ('wlu', 'Wilfred Laurier University'),
              ('york', 'York University')]

majorList = [('ba', 'Bachelor of Arts (B.A)'),
             ('basc', 'Bachelor of Applied Science (B.ASc.)'),
             ('bba', 'Bachelor of Business Adminstration (B.B.A.)'),
             ('bcom', 'Bachelor of Commerce (B.Comm)'),
             ('bmath', 'Bachelor of Math (B.Math)'),
             ('bsc', 'Bachelor of Science (B.Sc)')]

yearList = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]

industryList = [('acc', 'Accounting'),
             ('arc', 'Architecture and Planning'),
             ('auto', 'Automotive'),
             ('aero', 'Aviation and Aerospace'),
             ('bank', 'Banking'),
             ('broad', 'Broadcast Media'),
             ('cap', 'Capital Markets'),
             ('cs', 'Computer Software'),
             ('def', 'Defense and Space'),
             ('eng', 'Engineering'),
             ('fin', 'Financial Services'),
             ('gov', 'Government Administration')]

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class AdminRegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class MenteeRegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=0, max=64)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=0, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    headline = StringField('Headline', validators=[DataRequired(), Length(min=0, max=100)])
    about = StringField('About', validators=[Length(min=0, max=280)])
    skills = StringField('Skillset', validators=[Length(min=0, max=164)])
    university = SelectField(u'University', choices=schoolList, coerce=str)
    major = SelectField(u'Major', choices=majorList, coerce=str)
    year = SelectField(u'Year', choices=yearList, coerce=int)
    company = SelectField('Company', validators=[Length(min=0, max=164)])
    industry = SelectField(u'Industry', choices=industryList, coerce=str)
    linkedin = StringField('LinkedIn Link', validators=[Length(min=0, max=164)])
    twitter = StringField('Twitter Link', validators=[Length(min=0, max=164)])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class MentorRegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[Length(min=0, max=64)])
    last_name = StringField('Last Name', validators=[Length(min=0, max=64)])
    headline = StringField('Headline', validators=[DataRequired(), Length(min=0, max=100)])
    about = StringField('About', validators=[Length(min=0, max=280)])
    company = StringField('Current Company', validators=[Length(min=0, max=164)])
    position = StringField('Current Position', validators=[Length(min=0, max=164)])
    industry = SelectField(u'Industry', choices=industryList, coerce=str)
    university = SelectField(u'University', choices=schoolList, coerce=str)
    major = SelectField(u'Major', choices=majorList, coerce=str)
    grad_year = StringField('Year of Graduation', validators=[Length(min=0, max=64)])
    skills = StringField('Skillset', validators=[Length(min=0, max=164)])
    avail = StringField('Availability', validators=[Length(min=0, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    linkedin = StringField('LinkedIn Link', validators=[Length(min=0, max=164)])
    twitter = StringField('Twitter Link', validators=[Length(min=0, max=164)])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class EditMentorProfileForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=0, max=64)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=0, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    headline = StringField('Headline', validators=[DataRequired(), Length(min=0, max=100)])
    about = StringField('About', validators=[DataRequired(), Length(min=0, max=280)])
    avail = StringField('Availability', validators=[DataRequired(), Length(min=0, max=64)])
    skill = StringField('Skillset', validators=[DataRequired(), Length(min=0, max=164)])
    industry = SelectField(u'Industry', choices=industryList, coerce=str)
    company = StringField('Current Company', validators=[DataRequired(), Length(min=0, max=164)])
    position = StringField('Current Position', validators=[DataRequired(), Length(min=0, max=164)])
    university = SelectField(u'University', choices=schoolList, coerce=str)
    major = SelectField(u'Major', choices=majorList, coerce=str)
    grad_year = StringField('Year of Graduation', validators=[Length(min=0, max=64)])
    linkedin = StringField('LinkedIn Link', validators=[DataRequired(), Length(min=0, max=164)])
    twitter = StringField('Twitter Link', validators=[DataRequired(), Length(min=0, max=164)])
    submit = SubmitField('Save Profile')

    def __init__(self, original_email, *args, **kwargs):
        super(EditMentorProfileForm, self).__init__(*args, **kwargs)
        self.original_email = original_email

    def validate_email(self, email):
        if email.data != self.original_email:
            user = User.query.filter_by(email=self.email.data).first()
            if user is not None:
                raise ValidationError('Please use a different email address.')

class EditMenteeProfileForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=0, max=64)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=0, max=64)])
    headline = StringField('Headline', validators=[DataRequired(), Length(min=0, max=100)])
    about = StringField('About', validators=[DataRequired(), Length(min=0, max=280)])
    company = StringField('Company Name', validators=[DataRequired(), Length(min=0, max=100)])
    university = SelectField(u'University', choices=schoolList, coerce=str)
    major = SelectField(u'Major', choices=majorList, coerce=str)
    year = SelectField(u'Year', choices=yearList, coerce=int)
    industry = SelectField(u'Industry', choices=industryList, coerce=str)
    email = StringField('Contact Email', validators=[DataRequired(), Email()])
    skill = TextAreaField('Skillset', validators=[DataRequired(), Length(min=0, max=280)])
    linkedin = StringField('LinkedIn Link', validators=[DataRequired(), Length(min=0, max=164)])
    twitter = StringField('Twitter Link', validators=[DataRequired(), Length(min=0, max=164)])
    submit = SubmitField('Save Profile')

    def __init__(self, original_email, *args, **kwargs):
        super(EditMenteeProfileForm, self).__init__(*args, **kwargs)
        self.original_email = original_email

    def validate_email(self, email):
        if email.data != self.original_email:
            user = User.query.filter_by(email=self.email.data).first()
            if user is not None:
                raise ValidationError('Please use a different email address.')


class EditCohortProfileForm(FlaskForm):
    company_name = StringField('Company Name', validators=[DataRequired(), Length(min=0, max=100)])
    email = StringField('Contact Email', validators=[DataRequired(), Email()])
    member_names = StringField('Names of Members', validators=[DataRequired(), Length(min=0, max=280)])
    industry = SelectField(u'Industry', choices=industryList, coerce=str)
    help_needed = StringField('What type of help are you looking for?',validators=[DataRequired(), Length(min=0, max=280)])
    submit = SubmitField('Save Profile')

    def __init__(self, original_email, *args, **kwargs):
        super(EditCohortProfileForm, self).__init__(*args, **kwargs)
        self.original_email = original_email

    def validate_email(self, email):
        if email.data != self.original_email:
            user = User.query.filter_by(email=self.email.data).first()
            if user is not None:
                raise ValidationError('Please use a different email address.')


class ApplicationForm(FlaskForm):
    company_name = StringField('Company Name', validators=[DataRequired(), Length(min=0, max=100)])
    team_emails = StringField('Emails of Team Members', validators=[DataRequired(), Length(min=0, max=280)])
    founder_names = StringField('Names of Founders', validators=[DataRequired(), Length(min=0, max=280)])
    industry = StringField('Industry', validators=[DataRequired(), Length(min=0, max=280)])
    team_skills = TextAreaField('Founder Skillsets', validators=[DataRequired(), Length(min=0, max=280)])
    help_needed = StringField('What type of help are you looking for?', validators=[DataRequired(), Length(min=0, max=280)])
    interest = TextAreaField('Why are you interested in the mentorship program?', validators=[DataRequired(), Length(min=0, max=500)])
    gain = TextAreaField('What do you hope to gain by the end of the program?', validators=[DataRequired(), Length(min=0, max=500)])
    stage = StringField('What stage is your startup at?', validators=[DataRequired(), Length(min=0, max=100)])
    relation = StringField('What type of mentorship relationship are you looking for (i.e. longterm)?', validators=[DataRequired(), Length(min=0, max=280)])
    website = StringField('Website (optional)', validators=[Length(min=0, max=280)])
    business_docs = StringField('Please provide a link to any applicable business documents', validators=[DataRequired(), Length(min=0, max=380)]) 
    submit = SubmitField('Apply Now!')

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')

class MentorSelectForm(FlaskForm):
    mentor1 = StringField('First Choice', validators=[DataRequired(), Length(min=0, max=128)])
    mentor2 = StringField('Second Choice', validators=[DataRequired(), Length(min=0, max=128)])
    mentor3 = StringField('Third Choice', validators=[DataRequired(), Length(min=0, max=128)])
    submit = SubmitField('Save Preferences')

class MenteeMatchForm(FlaskForm):
    mentor = StringField('Mentor ID', validators=[DataRequired(), Length(min=0, max=128)])
    submit = SubmitField('Save Preferences')

    def validate_mentor(self, mentor):
        user = Mentor.query.filter_by(id=mentor.data).first()
        if user is None:
            raise ValidationError('Invalid mentor ID.')