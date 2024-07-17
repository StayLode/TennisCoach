from datetime import timedelta
import os
from django.test import TestCase
from django.contrib.auth.models import User
from essential.models import Course, Lesson, Purchase
from users.models import Profile

class PermissionAuthTestCase(TestCase):

    def setUp(self):
        # Crea un utente di prova
        self.user = User.objects.create_user(username='users', password='testpass')
        self.profile = Profile.objects.get(user=self.user)

        # Crea un secondo utente di prova
        self.user2 = User.objects.create_user(username='other', password='otherpass')
        self.profile2 = Profile.objects.get(user=self.user2)

        # Crea un corso di prova
        self.course = Course.objects.create(
            user=self.profile,
            title='Test Course',
            description='Test course description',
            category='Test',
            price=19.99
        )

        # Crea un altro corso di prova
        self.course2 = Course.objects.create(
            user=self.profile2,
            title='Other Course',
            description='Other course description',
            category='Other',
            price=29.99
        )
        
        # Crea una lezione di prova associata al corso
        self.lesson = Lesson.objects.create(
            course=self.course,
            title='Test Lesson',
            video=os.path.join('videos', 'unknown_video.mp4')
        )

        # Crea un'altra lezione di prova associata al secondo corso
        self.lesson2 = Lesson.objects.create(
            course=self.course2,
            title='Other Lesson',
            video=os.path.join('videos', 'unknown_video2.mp4')
        )

        # Crea un acquisto del corso da parte dell'utente di prova
        self.purchase = Purchase.objects.create(
            user=self.profile,
            course=self.course
        )

        # Crea una lezione, aggiunta al corso appena acquistato
        self.lesson3 = Lesson.objects.create(
            course=self.course,
            title='Other Lesson',
            video=os.path.join('videos', 'unknown_video3.mp4')
        )

    def test_has_permission_auth_course_purchased(self):
        # Verifica che la funzione ritorna True quando il corso è stato acquistato dall'utente
        result = self.profile.has_permession_auth('unknown_video.mp4')
        self.assertTrue(result)
    
    def test_has_permission_auth_course_created_by_user(self):
        # Verifica che la funzione ritorna True quando il corso è stato creato dall'utente, e quindi non acquistato
        result = self.profile2.has_permession_auth('unknown_video2.mp4')
        self.assertTrue(result)

    def test_has_permission_auth_course_not_purchased(self):
        # Verifica che la funzione ritorna False quando il corso non è stato acquistato
        result = self.profile.has_permession_auth('unknown_video2.mp4')
        self.assertFalse(result)

    def test_has_permission_auth_no_lesson_found(self):
        # Verifica che la funzione ritorna False quando nessuna lezione viene trovata
        result = self.profile.has_permession_auth('nonexistent_video.mp4')
        self.assertFalse(result)

    def test_has_permission_auth_course_added_after_purchase(self):
        # Verifica che la funzione ritorna True quando il corso è stato acquistato dall'utente, e la lezione è stata aggiunta dopo l'acquisto
        result = self.profile.has_permession_auth('unknown_video3.mp4')
        self.assertTrue(result)
