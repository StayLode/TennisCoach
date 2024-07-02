from django.test import TestCase, Client
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.utils import timezone
from .models import Course, Purchase
from users.models import Profile
from custom_payment.models import Payment
from django.contrib.auth.models import Group


class SaveCourseViewTest(TestCase):
    def setUp(self):
        # Creiamo il client di test
        self.client = Client()

        # Creiamo un utente
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user_profile = Profile.objects.get(user=self.user)

        # Creiamo un altro utente
        self.other_user = User.objects.create_user(username='otheruser', password='otherpassword')
        self.coach_group = Group.objects.create(name='Coach')
        self.coach_group.user_set.add(self.other_user) 
        self.other_user_profile = Profile.objects.get(user=self.other_user)

        # Creiamo un corso a pagamento
        self.course = Course.objects.create(title="Test Course", user=self.other_user_profile, price=90)

        # Creiamo un corso gratuito
        self.free_course = Course.objects.create(title="Free Course", user=self.other_user_profile, price=0)

    def test_save_course_not_logged_in(self):
        # Tenta di salvare un corso senza essere loggato
        response = self.client.post(reverse_lazy('essential:save_course', args=[self.course.id]))
        # Verifica il reindirizzamento alla pagina di login
        login_url = reverse_lazy('login') + '?auth=notok&next=' + reverse_lazy('essential:save_course', args=[self.course.id])
        self.assertRedirects(response, login_url)

    def test_save_not_existing_course(self):
        # Effettua il login come il proprietario del corso
        self.client.login(username='otheruser', password='otherpassword')
        # ID del corso non esistente
        NE_course_id = 32
        # Tenta di salvare il corso non esistente
        response = self.client.post(reverse('essential:save_course', args=[NE_course_id]))
        # Verifica che la risposta sia un reindirizzamento (302)
        self.assertEqual(response.status_code, 302)
        # Verifica che il reindirizzamento sia alla pagina 404
        self.assertEqual(response.url, reverse('404'))
        # Richiedi la pagina di destinazione e verifica che abbia status code 404
        follow_response = self.client.get(response.url)
        self.assertEqual(follow_response.status_code, 404)


    def test_save_own_course(self):
        # Effettua il login come il proprietario del corso
        self.client.login(username='otheruser', password='otherpassword')
        # Tenta di salvare il proprio corso
        response = self.client.post(reverse_lazy('essential:save_course', args=[self.course.id]))
        # Verifica il reindirizzamento alla pagina dei corsi creati
        self.assertRedirects(response, reverse_lazy('essential:createdcourses'))
        # Verifica che il messaggio di avviso sia presente
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Il corso è di tua proprietà!")

    def test_save_course_not_purchased(self):
        # Effettua il login come un altro utente
        self.client.login(username='testuser', password='testpassword')
        # Tenta di salvare un corso a pagamento senza averlo acquistato
        response = self.client.post(reverse_lazy('essential:save_course', args=[self.course.id]))
        # Verifica il reindirizzamento alla dashboard
        self.assertRedirects(response, reverse_lazy('users:dashboard'))
        # Verifica che il messaggio di errore sia presente
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Azione non consentita")

    def test_save_course_purchased(self):
        # Simula l'acquisto del corso
        Payment.objects.create(description=self.course.id, billing_first_name=self.user.username)
        # Effettua il login come l'utente che ha acquistato il corso
        self.client.login(username='testuser', password='testpassword')
        # Tenta di salvare il corso acquistato
        response = self.client.post(reverse_lazy('essential:save_course', args=[self.course.id]))
        # Verifica il reindirizzamento alla dashboard
        self.assertRedirects(response, reverse_lazy('users:dashboard'))
        # Verifica che il messaggio di successo sia presente
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Corso salvato con successo!")
        # Verifica che il corso sia stato salvato
        self.assertTrue(Purchase.objects.filter(user=self.user_profile, course=self.course).exists())

    def test_save_free_course(self):
        # Effettua il login come un altro utente
        self.client.login(username='testuser', password='testpassword')
        # Tenta di salvare un corso gratuito
        response = self.client.post(reverse_lazy('essential:save_course', args=[self.free_course.id]))
        # Verifica il reindirizzamento alla dashboard
        self.assertRedirects(response, reverse_lazy('users:dashboard'))
        # Verifica che il messaggio di successo sia presente
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Corso salvato con successo!")
        # Verifica che il corso gratuito sia stato salvato
        self.assertTrue(Purchase.objects.filter(user=self.user_profile, course=self.free_course).exists())

    def test_save_already_saved_course(self):
        # Simula che il corso sia già stato salvato
        Purchase.objects.create(user=self.user_profile, course=self.course, date=timezone.now())
        # Simula l'acquisto del corso
        Payment.objects.create(description=self.course.id, billing_first_name=self.user.username)
        # Effettua il login come l'utente che ha già salvato il corso
        self.client.login(username='testuser', password='testpassword')
        # Tenta di salvare nuovamente il corso
        response = self.client.post(reverse_lazy('essential:save_course', args=[self.course.id]))
        # Verifica il reindirizzamento alla dashboard
        self.assertRedirects(response, reverse_lazy('users:dashboard'))
        # Verifica che il messaggio di avviso sia presente
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Hai già salvato questo corso.")
