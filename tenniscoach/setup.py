import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tenniscoach.settings")
django.setup()

from tenniscoach.setup.initcmds import init_db, erase_db

erase_db()
init_db()