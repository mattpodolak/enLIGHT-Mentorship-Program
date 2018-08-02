
- [Getting Started](#getting-started)
    - [Setting Up](#setting-up)
    - [Install Packages](#install-packages)
    - [Running Your App](#running-your-app)
    - [Sending Mail](#sending-mail)
- [Database](#database)
    - [Database Testing](#database-testing)

# Getting Started

## Setting Up
Make new venv
```bash
> python -m venv mentorship-venv
```

Activate venv
```bash
> mentorship-venv\Scripts\activate
```

## Install Packages
Install required packages
```bash
> pip install flask
> pip install flask_sqlalchemy
> pip install flask_migrate
> pip install flask_wtf
```

## Running Your App
Set ENVIRONMENT variables
```bash
> set FLASK_APP=mentorship.py
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

## Database Testing
Run shell in diff terminal for db manipulation
```bash
> flask shell
```

Running into problems with db migration because u deleted a column?
```bash
> db.reflect()
> db.drop_all()
```

delete migration scripts by hand

Recreate migration scripts
```bash
> flask db migrate -m "message"
> flask db upgrade
```
