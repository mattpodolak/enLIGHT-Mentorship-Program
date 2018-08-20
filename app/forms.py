from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User, Application

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class MenteeRegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
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
    email = StringField('Email', validators=[DataRequired(), Email()])
    about_me = StringField('About', validators=[Length(min=0, max=280)])
    avail = StringField('Availability', validators=[Length(min=0, max=64)])
    skill = StringField('Skillset', validators=[Length(min=0, max=164)])
    industry = StringField('Industries', validators=[Length(min=0, max=164)])
    company = StringField('Current Company', validators=[Length(min=0, max=164)])
    position = StringField('Current Position', validators=[Length(min=0, max=164)])
    linked = StringField('LinkedIn Link', validators=[Length(min=0, max=164)])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class EditProfileForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=280)])
    submit = SubmitField('Submit')

    def __init__(self, original_email, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_email = original_email

    def validate_email(self, email):
        if email.data != self.original_email:
            user = User.query.filter_by(email=self.email.data).first()
            if user is not None:
                raise ValidationError('Please use a different email address.')

class ApplicationForm(FlaskForm):
    company_name = StringField('Company Name', validators=[DataRequired(), Length(min=0, max=100)])
    contact_email = StringField('Contact Email', validators=[DataRequired(), Email()])
    founder_names = StringField('Names of Founders', validators=[DataRequired(), Length(min=0, max=280)])
    industry = StringField('Industry', validators=[DataRequired(), Length(min=0, max=280)])
    team_skills = TextAreaField('Founder Skillsets', validators=[DataRequired(), Length(min=0, max=280)])
    help_needed = StringField('What type of help are you looking for?', validators=[DataRequired(), Length(min=0, max=280)])
    interest = TextAreaField('Why are you interested?', validators=[DataRequired(), Length(min=0, max=500)])
    gain = TextAreaField('What do you hope to gain?', validators=[DataRequired(), Length(min=0, max=500)])
    stage = StringField('What stage is your startup at?', validators=[DataRequired(), Length(min=0, max=100)])
    relation = StringField('What type of mentorship relationship are you looking for?', validators=[DataRequired(), Length(min=0, max=280)])
    website = StringField('Website (optional)', validators=[Length(min=0, max=280)])
    business_docs = StringField('Please provide a link to any applicable business documents', validators=[DataRequired(), Length(min=0, max=380)]) 
    submit = SubmitField('Apply')
    
    def validate_contact_email(self, contact_email):
        user = Application.query.filter_by(email=contact_email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
