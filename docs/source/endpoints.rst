Routes
=====

Register
------------



.. code-block:: console

   (.venv) $ python -m pip install -r requirements
   (.venv) $ python manage.py makemigrations
   (.venv) $ python manage.py migrate
   (.venv) $ python manage.py runserver

Responses
----------------

Login response success example : 
.. code-block:: console

    {
        "status": 200,
        "message": "Successfully logged in",
        "error": false,
        "pagination": false,
        "body": {
            "token": "6c3553912af1b3459be7c1d5833301df1c69f612"
        }
    }


