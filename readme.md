# The Memory App

Welcome to my 13th and last Project in OpenClassroom : The memory App

## What is it?

It's an application where you can create you own deck of flashcards or even search one to copy.

The method used is optimised for you to learn it in the long term.

## Getting Started

You can use this application at : https://the-memory-app.herokuapp.com/
or at http://46.101.230.219/

### Prerequistes

This application work with Python 3.7.3 and Django 3.0.5

This is set to use the default database of Django, but you're free to use your own SGDB and to configure it in settings.py

### Installing

Clone this repo 
```
git clone https://github.com/M0l42/OC_P13_Memory_App
```
Create the virtualenv

Install dependecies
```
pip install -r requirements.txt
```

Set the database and admin user
```
python manage.py migrate
python manage.py runscript load_database
python manage.py createsuperuser
```

Then you can run the app 
```
python manage.py runserver
```

## Built With

* [Django](https://www.djangoproject.com/)

## Special Shout-out

To [Fabien Olicard](https://www.fabienolicard.fr/) and his [Memory Box]( https://amzn.to/2yRCtsD) who inspired 
this project