from essential.models import Course, Lesson, Purchase
from users.models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

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

	#Creazione superuser
	admin = User.objects.create_superuser(username="admin", password="123")
	admin.save()

	#Creazione customers
	utenti_customer = ["matteo", "lode", "nicholas", "andrea"]
	for name in utenti_customer:
		customer = User.objects.create_user(username=name, password="123")
		g = Group.objects.get(name="Customer") 
		g.user_set.add(customer) 
		customer.save()

	#Creazione coaches
	utenti_coach = ['mezzanotte', 'prampolini', 'ugolini', 'menabue']

	for name in utenti_coach:
		coach = User.objects.create_user(username=name, password="123")
		g = Group.objects.get(name="Coach") 
		g.user_set.add(coach) 
		coach.save()

	#Creazione corsi
	categories = ["Principiante", "Intermedio", "Esperto"]
	coaches =  list(User.objects.filter(username__in=utenti_coach))
	for course in courses_data:
		coach_id = random.randint(0,3)
		category_val = random.randint(0,2)
		picture_id = random.randint(1,5)
		c = Course()
		c.title = course["titolo"]
		c.description = course["descrizione"]
		c.user = coaches[coach_id]
		c.category = categories[category_val]
		c.price = course["prezzo"]
		c.picture = os.path.join('images', f'unknown_course{picture_id}.jpg')
		c.save()
		#Aggiunta lezioni
		for lesson in course["lezioni"]:
			l = Lesson()
			l.title = lesson["titolo"]
			min, sec = map(int,  lesson["durata"].split(':'))
			duration = timedelta(minutes=min, seconds=sec)
			l.duration = duration
			l.course = c
			l.save()
                

    
	print("DUMP DB")
