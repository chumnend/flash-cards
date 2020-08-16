# Flashcards
A web app for creating and managing flashcards, built using Django/Python. The idea of this 
project was to experiment with building a social media like application while also learning 
more about the Django ecosystem.

## Development Setup

### Prerequistes
- Python 3
- Pip
- virtualenv
- Postgresql

### Start
Setup virtual environment,
```
python3 -m virtualenv venv
source venv/bin/activate
```

Install dependencies,
```
pip install -r requirements.txt
```

Copy env.example into .env file and fill it out,
```
cp env.example .env
```

```
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

Change to source directory,
```
cd src/
```

Collect staticfiles,
```
python manage.py collectstatic
```

Run any migrations,
```
python manage.py migrate
```

Start the app,
```
python manage.py runserver <PORT>
```

### Test
```
python manage.py test
```

### Scripts
The 'run.sh' script can be used to automatically collect static files, migrate 
the database and run the app in one console call,
```
./run.sh
```

### Deploy
Push to master branch to deploy to Heroku
