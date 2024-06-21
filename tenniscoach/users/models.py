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
    picture = models.ImageField(
        upload_to='users_pics',
        default=os.path.join('static/images', 'unknown_user.jpg'),
        blank=True
    )
    description = models.CharField(max_length=1000, null=True)
        
    def __str__(self):
        pass

    class Meta:
        verbose_name_plural = "Utenti"