Platform core backend
===

## Branch for DevOps developers

### Docker
** Dockerfile is coded for development purpose. It doesn't cover database migrate action and still uses .env to retrieve secrets.

Build image (for initial setup):
    ```bash
    $ docker build -f Dockerfile -t django_azure:latest .
    ```

1. Run image:
    ```bash
    $ docker run -p 8002:8002 -it django_azure .
    ```

2. Then access application via `localhost:8002`

3. To test the application, go to `localhost:8002/login`. Complete your login with Azure then go to `localhost:8002/api/v1/me`. Then you should see your Azure information in Json format in the browser.


## Scope of shgp-backend-core

The core contains the main backend framework of the platform. It connects to microservices and API endpoints used by the platform.


## Software Requirements

* Python 3.7


## Initial Setup

1. Create a virtual environment for the backend:
    ```bash
    $ cd shgp-backend-core
    $ python3 -m venv venv
    $ source venv/bin/activate
    ```
2. Once in your virtual environment, run:
    ```bash
    $ pip install -r requirements.txt
    ```
3. Migrate Django Models:
    ```bash
    python manage.py migrate
    python manage.py createcachetable

    OR

    ./nuke_db.sh
    ```

## Django
1. To run the django backend, activate the virtual environment:
    ```bash
    $ source venv/bin/activate
    ```
2. Then run server:
    ```bash
    $ python manage.py runserver
    OR
    $ ./manage.py runserver
    ```
3. Once the server is up, in browser, use `http://localhost:8000/`to explore the backend APIs.
