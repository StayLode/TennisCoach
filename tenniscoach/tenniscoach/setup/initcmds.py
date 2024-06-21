from essential.models import Course, Lesson, Purchase
from users.models import Profile
from django.contrib.auth.models import User
from datetime import timedelta
import json, os, random
from django.db import connection

from pathlib import Path

FILENAME: str = "corsi.json"
FILEPATH: str = os.path.join(
	Path(__file__).resolve().parent,
	FILENAME
)

def reset_ids(tables):
	for t in tables:
		with connection.cursor() as cursor:
			cursor.execute(f"DELETE FROM sqlite_sequence WHERE name = '{t}';")


def erase_db():
	print("Cancello il DB")
	Purchase.objects.all().delete()

	Course.objects.all().delete()
	Profile.objects.all().delete()
	Lesson.objects.all().delete()
	User.objects.all().delete()

def init_db():
	tables=["auth_user","essential_course","essential_lesson","users_profile","essential_purchase"]
	reset_ids(tables)

	if Course.objects.count()!= 0:
		return
    
	with open(FILEPATH, encoding='utf-8') as f:
		courses_data = json.load(f)

	admin = User.objects.create_superuser(username="admin", password="123")
	admin.save()

	user = User.objects.create_user(username="lode", password="123")
	user.save()

	coaches=['mezzanotte', 'prampolini', 'ugolini', 'menabue']
	categories = ["Principiante", "Intermedio", "Esperto"]

	for name in coaches:
		user = User.objects.create_user(username=name, password="123")
		user.save()

	users =  list(User.objects.all())

	for course in courses_data:
		coach_id = random.randint(1,4)
		category_val = random.randint(0,2)
		picture_id = random.randint(1,5)
		c = Course()
		c.title = course["titolo"]
		c.description = course["descrizione"]
		c.user = users[coach_id]
		c.category = categories[category_val]
		c.price = course["prezzo"]
		c.picture = os.path.join('static/images', f'unknown_course{picture_id}.jpg')
		c.save()

		for lesson in course["lezioni"]:
			l = Lesson()
			l.title = lesson["titolo"]
			min, sec = map(int,  lesson["durata"].split(':'))
			duration = timedelta(minutes=min, seconds=sec)
			l.duration = duration
			l.course = c
			l.save()
                

    
	print("DUMP DB")
	#print(Libro.objects.all()) #controlliamo
	#print(Copia.objects.all())
