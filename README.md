Waterloo Math Orientation Website
===

Official website of the University of Waterloo Math Faculty Orientation Week.

## Getting Started

Make you have some recent version of Python installed on your system.
Optionally use [pyenv](https://github.com/yyuu/pyenv) to manage your Python
installation (install Python version 3.5.1).

Install Django by opening the command line and running

```
pip install Django==1.9.7
```

Next, install Node.js. [Download here](https://nodejs.org/en/) or install via
your favourite package manager.

Install [Bower](https://bower.io) via command line. This will be used for
front-end package management

```
npm install -g bower
```

Install necessary dependencies

```
pip install -r requirements.txt
bower install
```

Migrate SQLite database

```
python manage.py migrate
```

## Running the server

Navigate to the directory where this repo is cloned and run

```
python manage.py runserver
```

This will boot up the server at http://127.0.0.1:8000/.

## Deployment

### Environment setup

You'll need to create a `.env` file on the production server before deploying
for the first time. Use this template:

```
DJANGO_ENVIRONMENT=production
SECRET_KEY=<Django Secret Key>
FACEBOOK_APP_ID=<Facebook App ID>
FACEBOOK_APP_SECRET=<Facebook App Secret>
```

### Asset Compilation

TODO
