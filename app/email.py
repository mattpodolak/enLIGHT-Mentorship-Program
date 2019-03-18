from flask_mail import Message
from app import mail
from flask import render_template
from app import flapp
from threading import Thread

def send_async_email(app, msg):
    with flapp.app_context():
        mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(flapp, msg)).start()

def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email('[enLIGHT Mentorship] Reset Your Password',
               sender=flapp.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('email/reset_password.html',
                                         user=user, token=token))

def accept_applicant(user, app):
    send_email("[enLIGHT Mentorship] Congratulations!",
               sender=flapp.config['ADMINS'][0],
               recipients=[app.email],
               text_body=render_template('email/accept_applicant.txt',
                                         user=user, app=app),
               html_body=render_template('email/accept_applicant.html',
                                         user=user, app=app))

def match_mentee(user, mentee):
    send_email("[enLIGHT Mentorship] You have a match!",
               sender=flapp.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/match_mentee.txt',
                                         user=user, mentee=mentee),
               html_body=render_template('email/match_mentee.html',
                                         user=user, mentee=mentee))

def contact_email(name, email, subject, message):
    send_email("[enLIGHT Mentorship] Contact Form",
               sender=flapp.config['ADMINS'][0],
               recipients=["mpodola2@gmail.com"],
               text_body=render_template('email/contact.txt',
                                         name=name, email=email, subject=subject, message=message),
               html_body=render_template('email/contact.html',
                                         name=name, email=email, subject=subject, message=message))
