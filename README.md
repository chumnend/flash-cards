# Flashcards
A web app for creating and managing flashcards, built using Django/Python

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

### Deploy
Push to master branch to deploy to Heroku
