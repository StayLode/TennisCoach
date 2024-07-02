from django.db import models
from django.contrib.auth.models import User
import os
from moviepy.editor import VideoFileClip
from django.utils import timezone
from users.models import Profile
from django.core.validators import MinValueValidator
from django.db.models import UniqueConstraint


class Course(models.Model):
    """
    Entity that models a course, composed by lessons.
    """
    
    user = models.ForeignKey(Profile,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    picture = models.ImageField(
        upload_to='static/courses_pics/',
        default='/static/images/unknown_course1.jpg',
        blank=True
    )
    category = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=4, decimal_places=2, validators=[MinValueValidator(0)])  
    date = models.DateTimeField(auto_now_add=True)      
    
    def isFree(self):
        return not(bool(self.price))
    
    def getTitle(self):
        return self.title[:45]+"..." if len(self.title)>50 else self.title


    class Meta:
        verbose_name_plural = "Corsi"
    
    def __str__(self):
        return f"{self.title} - {self.user.user} - ({self.date.strftime('%Y-%m-%d')})"
    

class Lesson(models.Model):
    """
    Entity that models a lesson.
    """
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    duration = models.DurationField(blank=True, null=True)
    video = models.FileField(
        upload_to='courses_videos/',
        default=os.path.join('videos', 'unknown_video.mp4'),
        blank=True
    ) 
    
    def save(self, *args, **kwargs):
        # Calcola la durata del video solo se è impostato il video
        super().save(*args, **kwargs)
        
        
        if self.video:
            try:
                video_path = self.video.path
                clip = VideoFileClip(video_path)
                self.duration = timezone.timedelta(seconds=clip.duration)
                Lesson.objects.filter(pk=self.pk).update(duration=self.duration)
            except OSError as e:
                print(f"Errore nel caricare il video: {e}")


   
    class Meta:
        verbose_name_plural = "Lezioni"

    def __str__(self):
        return f"{self.title} ({self.course.title})"

class Purchase(models.Model):    
    """
    Entity that describe the relationship between user and course and models a purchase of a course.
    """
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.user}: {self.user.name} {self.user.surname} - {self.course.title} ({self.date.strftime('%Y-%m-%d')})"
    
    class Meta:
        constraints = [
            UniqueConstraint(fields=['user', 'course'], name='unique_user_course')
        ]
        verbose_name_plural = "Acquisti"


