Django API Bootstrap with Authentication
=========================

Django Rest Framework API bootstrap with authentication features,
auto generated API documentation and administration panel.

Installation
-------

This project was created with `python3.10.6`.
Based on authentication token.

### Create a python virtual environment
```python3 -m venv ENV_NAME```

### Load virtual environment
```source ENV_NAME/bin/activate```

### Install requirements
```pip install -r requirements.txt```

### Prepare Database migrations
```./manage.py makemigrations```

### Migrate Database
```./manage.py migrate```

### Create Admin user
 ```./manage.py createsuperuser```

### Lauch Dev server
```./manage.py runserver```

### Set SMTP informations
It requires to set mail informations in `settings.py`, it allows application to send link during register or password reset process.

```
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = "example@gmail.com"
EMAIL_HOST_PASSWORD = "apikey"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
```


Routes
-------

- Login
- Logout
- Register
- Password Reset
- Password Update
- Email Validation
- Profile
- Deactivate account

When dev server is lauched, visit http://localhost:8000/api/v1/documentation/

Responses
-------

All API routes reponses have a generic json struct, with `status`, `message`, `error`, `body`. 

Login example : 
```
{

    "status": 200,
    "message": "Successfully logged in",
    "error": false,
    "body": {
        "token": "6c3553912af1b3459be7c1d5833301df1c69f612"
    }

}
```
```
{

    "status": 400,
    "message": "Your request can't be perfomed",
    "error": true,
    "body": {
        "non_field_errors": [
            "Unable to log in with provided credentials."
        ]
    }

}
```


Administration
-------
When dev server is lauched, visit http://localhost:8000/admin/

Requirements
-----
django, djangorestframework, coreapi, coreapi-cli, pyyaml
