# Flashcards

## About This Project

A web app for creating and managing flashcards, built using **Django/Python**. The idea of this
project was to experiment with building a social media like application while also learning
more about the Django ecosystem.

### Demo

![Flashcards demo video](flashcards-capture.gif)

### Built With

- Python 3
- PostgreSQL

## Getting Started

1) Clone the repo,

```sh
git clone git@github.com:chumnend/flash-cards.git
```

2) Setup virtual environment,

```sh
python3 -m virtualenv venv
source venv/bin/activate
```

3) Install dependencies,

```sh
pip install -r requirements.txt
```

4) Copy env.example into .env file and fill it out,

```sh
cp env.example .env
```

```sh
# .env example
SECRET_KEY=secret
DATABASE_URL=postgres://<db_user>:<db_password>@127.0.0.1:5432/<db_name>
ALLOWED_HOSTS=*
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=
EMAIL_PORT=
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
EMAIL_USE_TLS=
```

5) Change to source directory,

```sh
cd src/
```

6) Collect staticfiles,

```sh
python manage.py collectstatic
```

7) Run any migrations,

```sh
python manage.py migrate
```

8) Start the app,

```sh
python manage.py runserver <PORT>
```

9) Test the app by running the following command,

```sh
python manage.py test
```

10) The `run.sh` script can be used to automatically collect static files, migrate 
the database and run the app in one console call,

```sh
./run.sh
```

### Deployment

Not deployed.

## Contact

Nicholas Chumney - [nicholas.chumney@outlook.com](nicholas.chumney@outlook.com)
