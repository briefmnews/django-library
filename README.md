# django-esidoc
[![Python 3.10](https://img.shields.io/badge/python-3.8|3.9|3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/) 
[![Django 3.2](https://img.shields.io/badge/django-3.2-blue.svg)](https://docs.djangoproject.com/en/3.2/)
[![Python CI](https://github.com/briefmnews/django-library/actions/workflows/workflow.yaml/badge.svg)](https://github.com/briefmnews/django-library/actions/workflows/workflow.yaml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)  
Handle CAS login via sso for french libraries (C3RB, GMInvent and Archimed).

## Installation
Install with [pip](https://pip.pypa.io/en/stable/):
```shell
pip install -e git://github.com/briefmnews/django-library.git@main#egg=django-library
```

## Setup
In order to make `django-library` works, you'll need to follow the steps below.

### Settings
First you need to add the following configuration to your settings:
```python
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',

    'django_library',
    ...
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    
    'django_library.middleware.CASMiddleware',
    ...
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    
    'django_library.backends.CASBackend',
    ...
)
```

### Migrations
Next, you need to run the migrations in order to update your database schema.
```shell
python manage.py migrate
```

### Mandatory settings
Here is the list of all the mandatory settings:
```python
LIBRARY_GMINVENT_BASE_URL
LIBRARY_C3RB_BASE_URL
LIBRARY_ARCHIMED_BASE_URL
LIBRARY_QUERY_STRING_TRIGGER
```

### Optional settings - Default redirection
You can set a default path redirection for inactive user by adding this line to 
your settings:
```python
LIBRARY_INACTIVE_USER_REDIRECT = '/{mycustompath}/'
```
`LIBRARY_INACTIVE_USER_REDIRECT` is used if an inactive user with a valid ticket
tries to login.
If `LIBRARY_INACTIVE_USER_REDIRECT` is not set in the settings, it will take
the root path (i.e. `/`) as default value.


## How to use ?
Once your all set up, when a request to your app is made with the query string 
`library_sso_id=<unique_sso_id>`, the `CASMiddleware` catches the request and start the login process. 
Here is an example of a request url to start the login process:
```
https://www.exemple.com/?library_sso_id=briefme
```

## Tests
Testing is managed by `pytest`. Required package for testing can be installed with:
```shell
pip install -r test_requirements.txt
```
To run testing locally:
```shell
pytest
```

## Credits
- [python-cas](https://github.com/python-cas/python-cas)
- [django-cas-ng](https://github.com/mingchen/django-cas-ng)

## References
- [CAS protocol](https://www.apereo.org/projects/cas)
