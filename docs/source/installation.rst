Installation
=====

To use Django API

.. code-block:: console

   (.venv) $ python -m pip install -r requirements
   (.venv) $ python manage.py makemigrations
   (.venv) $ python manage.py migrate
   (.venv) $ python manage.py runserver

.. Responses
.. ----------------

.. Login response success example : 
.. .. code-block:: console

.. {
..     "status": 200,
..     "message": "Successfully logged in",
..     "error": false,
..     "pagination": false,
..     "body": {
..         "token": "6c3553912af1b3459be7c1d5833301df1c69f612"
..     }
.. }

.. To retrieve a list of random ingredients,
.. you can use the ``lumache.get_random_ingredients()`` function:

.. .. autofunction:: lumache.get_random_ingredients

.. The ``kind`` parameter should be either ``"meat"``, ``"fish"``,
.. or ``"veggies"``. Otherwise, :py:func:`lumache.get_random_ingredients`
.. will raise an exception.

.. .. autoexception:: lumache.InvalidKindError


