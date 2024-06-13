from django.db import models
from django.contrib.auth.models import User
import os
# Create your models here.

class Profile(models.Model):
    """
    Entity that models a profile.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    picture = models.ImageField(
        upload_to='users_pics',
        default=os.path.join('static', 'unknown_user.png'),
        blank=True
    )
    description = models.CharField(max_length=1000)
        
    def __str__(self):
        pass

    class Meta:
        verbose_name_plural = "Utenti"

class Course(models.Model):
    """
    Entity that models a course, composed by lessons.
    """
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)
    picture = models.ImageField(
        upload_to='courses_pics',
        default=os.path.join('static', 'unknown_course.png'),
        blank=True
    )
    price = models.DecimalField(decimal_places=2, null=True, blank=True)        
    def __str__(self):
        pass

    class Meta:
        verbose_name_plural = "Corsi"

class Lesson(models.Model):
    """
    Entity that models a lesson.
    """
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    duration = models.CharField(max_length=1000)
    picture = models.FileField(
        upload_to='courses_videos/',
        default=os.path.join('static', 'unknown_course.png'),
        blank=True
    )
    price = models.DurationField()        
    def __str__(self):
        pass

    class Meta:
        verbose_name_plural = "Lezioni"

class Purchase(models.Model):    
    """
    Entity that describe the relationship between user and course and models a purchase of a course.
    """
    utente = models.ForeignKey(User, on_delete=models.PROTECT)
    corso = models.ForeignKey(Course, on_delete=models.PROTECT)
    date = date = models.DateTimeField()

    def purchased_by(self):
        if self.utente == None: return None
        return self.utente.username
    
    class Meta:
        verbose_name_plural = "Acquisti"
