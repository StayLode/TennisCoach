from django.db import models
import os
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, *args, **kwargs):
  if created:
    Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
  instance.profile.save()

class Profile(models.Model):
    """
    Entity that models a profile.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, null=True)
    surname = models.CharField(max_length=20, null=True)
    email = models.EmailField(null = True)
    description = models.CharField(max_length=400, null=True, blank=True)
    picture = models.ImageField(
        upload_to='static/users_pics',
        default='/static/images/unknown_user.jpg',
        blank=True
    )
    purchases = models.ManyToManyField(to = "essential.Course", through="essential.Purchase", blank=True, related_name="profile_purchases")


    def __str__(self):
      return f"{self.user}: {self.name} {self.surname} ({self.email})"

    class Meta:
        verbose_name_plural = "Profili utente"


    def has_permession_auth(self, resource:str):
      #L'import va fatto dentro in modo che sia lazy; così facendo quando richiamo has_permession_auth Lesson sarà definita
      from essential.models import Lesson
      lesson = Lesson.objects.filter(video__icontains=resource)
      if not lesson:
        return False
      
      # Tra tutti i corsi che contengono la risorsa controllo se ce n'è almeno uno che è acquistato
      if lesson.filter(course__pk__in=self.purchases.values('pk')):
        return True
      
      if lesson.filter(course__user_id=self.user.id):
        return True
      return False