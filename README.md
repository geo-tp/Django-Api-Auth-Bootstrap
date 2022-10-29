Django API Bootstrap with Authentication
=========================

Django Rest Framework API bootstrap with authentication features,
auto generated API documentation and administration panel.

Installation
-------

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

### Lauch Dev server
```./manage.py runserver```

### Create Admin user
 ```./manage.py createsuperuser```

Routes
-------
When dev server is lauched, visit http://localhost:8000/api/v1/docs

Administration
-------
When dev server is lauched, visit http://localhost:8000/admin

Requirements
-----
django, djangorestframework, coreapi, coreapi-cli, pyyaml
