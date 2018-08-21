
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
- [Website Info](#website-info)
    - [Mentors](#mentors)
    - [Mentees](#mentees)

# Getting Started

## Creating Project
```bash
> git clone https://github.com/mattpodolak/enLIGHT-Mentorship-Program.git
> git remote add origin https://github.com/mattpodolak/enLIGHT-Mentorship-Program.git
```

## Setting Up
Make new venv
```bash
> python -m venv mentorship-venv
```

Install required packages
```bash
> pip install -r requirements.txt
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

Add these ENVIRONMENT variables for Mail capabilities
```bash
> set MAIL_SERVER=smtp.googlemail.com
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
> flask shell
> from app import db
> from app.models import ModelName
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