# Flashcards
A web app for creating and managing flashcards, built using Django/Python

## Development Setup

### Prerequistes
- Install Python 3
- Install Pip
- install virtualenv

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

Run any migartions,
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
