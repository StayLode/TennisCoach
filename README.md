# TennisCoach project

TechWeb Programmaing Project, based on Django.

This project aims to revolutionize tennis learning by creating a robust, scalable, and user-friendly platform for purchasing and accessing high-quality online courses

## Required Libraries

django==5.0.6; -> framework principale utilizzato per sviluppare l'applicazione web

django-bootstrap5==24.2; -> integra Bootstrap 5 con Django

django-braces==1.15.0 -> fornisce un insieme di mixins che facilitano l'implementazione di funzionalità comuni nelle viste class-based (CBV) di Django, come il controllo dell'appartenenza ad un gruppo.

django-crispy-forms==2.2; -> facilita la gestione dei form Django
django-payments==2.0.0; -> fornisce un'astrazione comune per gestire pagamenti online con diversi provider di pagamento
moviepy==1.0.3; -> libreria usata per gestire i video ed estrarne la lunghezza
pillow==10.4.0; -> libreria usata per l'elaborazione delle immagini
stripe==10.1.0; -> SDK ufficiale di Stripe per Python, utilizzata per interagire con l'API di Stripe e gestire pagamenti

## Setup

Follow these steps to set up and run the application:

### 1. Cloning
```bash
git clone https://github.com/StayLode/TennisCoach.git
cd TennisCOach
```
### 2. Install pipenv

Make sure pipenv is installed.
Locally install dependencies, then open virtual-environment shell with:

```bash
pipenv install
pipenv shell
```
### 3. Install the requirements
Install all project dependencies listed in the requirements.txt file:
```bash
pip install -r requirements.txt
```
### 4. Configure the database
Run the migrations to set up the database:
```bash
python manage.py makemigrations
python manage.py migrate
```
### 5. Populate DB:
Uncomment line with erase_db in tenniscoach/urls.py. It will insert random entries in your SqliteDB.
Once creation is finished, re-comment this line.

### 6. Start the server, only in development mode:
Start the Django server:
```bash
python manage.py runserver
```
### 7. Usage
Once the server is running, you can access the online tennis courses and use the available features.
Go to http://localhost:8000/ and start exploring.

