
- [Getting Started](#getting-started)
    - [Creating Project](#creating-project)
    - [Setting Up](#setting-up)
    - [Running Your App](#running-your-app)
    - [Sending Mail](#sending-mail)
- [Database](#database)
    - [Initiate Database](#initiate-database)
    - [Database Migration](#database-migration)
    - [Database Testing](#database-testing)
- [Issue Management](#issue-management)
- [Troubleshooting](#troubleshooting)
- [Website Info](#website-info)
    - [Mentors](#mentors)
    - [Mentees](#mentees)

# Getting Started

## Creating Project
```bash
> git clone https://github.com/mattpodolak/enLIGHT-Mentorship-Program.git
> git remote add origin https://github.com/mattpodolak/enLIGHT-Mentorship-Program.git
```

Make sure you are inside the folder before you continue, you can do this with the cd command

## Setting Up
Make new venv
```bash
> python -m venv mentorship-venv
```

Activate venv
```bash
> mentorship-venv\Scripts\activate
> source mentorship-venv/bin/activate // for Mac users
```

Install required packages
```bash
> pip install -r requirements.txt
```

Set environment variable
```bash
> set FLASK_APP=mentorship.py // export for Mac
```

Initiate database (not needed)
```bash
> flask db init
```

Update database
```bash
> flask db upgrade
```

Change to debug/development mode
```bash
> set FLASK_ENV=development // export for Mac users
```

## Running Your App
Activate venv
```bash
> mentorship-venv\Scripts\activate
> source mentorship-venv/bin/activate // for Mac users
```

Set ENVIRONMENT variables
```bash
> set FLASK_APP=mentorship.py //use export if on Mac
```

Add these ENVIRONMENT variables for Mail capabilities
```bash
> set MAIL_SERVER=smtp.googlemail.com //use export if on Mac
> set MAIL_PORT=587
> set MAIL_USE_TLS=1
> set MAIL_USERNAME=pythonbugemail@gmail.com
> set MAIL_PASSWORD=your-gmail-password
```

Update Database (only if db changes made by someone else)
```bash
> flask db upgrade
```

Run app
```bash
> flask run
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
> mentorship-venv\Scripts\activate
> source mentorship-venv/bin/activate // for Mac users
> flask shell
> from app import db
> from app.models import ModelName
```

Create admin account
Run shell in diff terminal for db manipulation
```bash
> mentorship-venv\Scripts\activate
> source mentorship-venv/bin/activate // for Mac users
> flask shell
> from app import db
> from app.models import User
> user = User(email="email", access=2)
> user.set_password("password")
> user.set_id()
> db.session.add(user)
> db.session.commit()
```

Close shell
```bash
> Ctrl+Z and Enter
```

Running into problems with db migration because u deleted a column? 

Do the following OR delete app.db
```bash
> db.reflect()
> db.drop_all()
```
Now, delete migration scripts by hand and redo migration

# Email
## Email Testing
Run shell in diff terminal for db manipulation
```bash
> mentorship-venv\Scripts\activate
> flask shell
> from flask_mail import Message
> from app import mail
```

# Issue Management
1. Pick an issue to address
2. Create a new branch (Pick a branchname that reflects the issue)
```bash 
> git branch branchname
``` 
3. Checkout branch 
```bash 
> git checkout branchname
```
4. When issue is solved, 'comment and close' issue on GitHub
5. Commit all changes on branchname using the Visual Studio Code Source Control
6. Checkout master 
```bash 
> git checkout master
```
7. Ensure master is up-to-date 
```bash 
> git pull
```
8. Merge branchname with master (If any merge conflicts, resolve and commit)
```bash 
> git merge branchname
``` 
9. Push updated master to GitHub 
```bash 
> git push
```
10. Delete branchname 
```bash 
> git branch -d branchname
```

Git command cheatsheet: https://gist.github.com/davfre/8313299
Git branch & merge info: https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging

# Troubleshooting

## Bad Request 400
- First check to see if you are running in development mode, if not set the following environment variable:
Change to debug mode
```bash
> set FLASK_ENV=development // export for Mac users
```
- Still having a "bad request 400" issue? Try running in incognito or clearing your browser cache or browser history

# Website Info

## Mentors

### What we are looking for
- Variety of industries and companies
- Serious about the time committment 
- Preferably people with experience working as a mentor or with startups

### Profile Page
- Name
- One line description
- Availability (hours/month)
- Skillset
- Industry
- Company and Position (under name)
- LinkedIn profile
- Relevant experience (optional)

## Mentees

### What we are looking for
- Pre-seed / seed stage startups

### Onboarding
- Apply first and make profile when accepted
- Can see mentor list and can rank preferences
- Fill out profile and will be matched with mentor within 7 days

### Profile Page
- Company name
- Founder names
- Industry
- Founder skillsets
- What type of help looking for

### Application
- Why are you interested?
- What do you hope to gain?
- What stage is your startup at
- What type of mentorship relationship are you looking for? (answer a couple questions, formal advisor, etc)
- Website (optional)
- Please provide a link to any applicable business documents

### TO DO
- add removal from shortlist
- add conditional link for shortlist on mentor list (based on if shortlisted or not) - Shortlist link appears if not on shortlist, Remove from Shortlist if on shortlist
- add Remove from Shortlist to mentor_shortlist
- repeat all of the above for mentee shortlist

- check what email work needs to be done
- link application acceptance to cohort accounts
- review what else needs to be done