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
 ```./manage.py createsuperuser```.

Routes
-------
When dev server is lauched, visit http://localhost:8000/api/v1/docs

Admininistration
-------
When dev server is lauched, visit http://localhost:8000/admin

Requirements
-----

#### asgiref==3.5.2
#### backports.zoneinfo==0.2.1
#### Django==4.1.2
#### djangorestframework==3.14.0
#### pytz==2022.5
#### sqlparse==0.4.3

