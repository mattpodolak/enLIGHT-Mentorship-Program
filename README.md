
- [Getting Started](#getting-started)
    - [Setting Up](#setting-up)
    - [Running Your App](#running-your-app)
    - [Sending Mail](#sending-mail)
- [Database](#database)
    - [Initiate Database](#initiate-database)
    - [Database Migration](#database-migration)
    - [Database Testing](#database-testing)
- [Pages](#pages)

# Getting Started

## Setting Up
Make new venv
```bash
> python -m venv mentorship-venv
```

Install required packages
```bash
> pip install flask
> pip install flask-sqlalchemy
> pip install flask-migrate
> pip install flask-wtf
> pip install flask-login
```

Initiate database (not sure if needed)
```bash
> flask db init
```

## Running Your App
Activate venv
```bash
> mentorship-venv\Scripts\activate
```

Set ENVIRONMENT variables
```bash
> set FLASK_APP=mentorship.py
```

Update Database
```bash
> flask db upgrade
```

Run app
```bash
> flask run
```
## Sending Mail
Add these ENVIRONMENT variables along
```bash
> set MAIL_PORT=587
> set MAIL_USE_TLS=1
> set MAIL_USERNAME=<your-gmail-username>
> set MAIL_PASSWORD=<your-gmail-password>
```

# Database 

## Initiate Database
```bash
> flask db init
```

## Database Migration
Perform database migrations when adding/changing columns
```bash
> flask db migrate -m "message here"
> flask db upgrade
```
Undo a migration with:
```bash
> flask db downgrade
```

## Database Testing
Run shell in diff terminal for db manipulation
```bash
> flask shell
```

Running into problems with db migration because u deleted a column? OR delete app.db
```bash
> db.reflect()
> db.drop_all()
```
Now, delete migration scripts by hand and redo migration

# Pages
- Mentorship Profile page
- Mentee Profile page
- Dashboard to see list of potential mentors/mentees