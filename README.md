# Blog App

Fullstack Django blog app implemented using Django 3 with MVT (Model-View-Template) architecture and CVBs (Class-Based-Views).

Hosted example: https://blog-app-django-fullstack.herokuapp.com/

Test Credentials:

    Username: test
    Password: testpassword

### Install

    $ pipenv install

### Setup

#### Migrations

    $ pipenv shell
    $ python manage.py migrate

### Run

    $ pipenv shell
    $ python manage.py runserver

### Deploy to Heroku

Create a Heroku app:
    $ heroku create <app-name>

Set up Heroku Remote Git:
    $ git remote set-url heroku <remote-heroku-git-url>


Push to Heroku for Deployment:
    $ git push heroku master

NOTE: make sure all changes are commit to git before running this command

Creating the PostgreSQL DB:
    $ heroku addons:create heroku-postgresql:hobby-dev --app=<app-name>

Apply Migrations to PostgreSQL DB:
    $ heroku run python manage.py migrate

Create Superuser:
    $ heroku run python manage.py createsuperuser