from django.db import models
from django.contrib.auth.models import User
import os
from moviepy.editor import VideoFileClip
from django.utils import timezone



class Course(models.Model):
    """
    Entity that models a course, composed by lessons.
    """
    
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)
    picture = models.ImageField(
        upload_to='courses_pics',
        default=os.path.join('static/images', f'unknown_course1.jpg'),
        blank=True
    )
    category = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=4, decimal_places=2)  
    date = models.DateTimeField(auto_now_add=True)      
    def __str__(self):
        pass
    def isFree(self):
        return not(bool(self.price))
    
    def getTitle(self):
        return self.title[:45]+"..." if len(self.title)>50 else self.title


    class Meta:
        verbose_name_plural = "Corsi"
    
    

class Lesson(models.Model):
    """
    Entity that models a lesson.
    """
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    duration = models.DurationField(max_length=1000)
    videos = models.FileField(
        upload_to='courses_videos/',
        default=os.path.join('static/videos', 'unknown_video.mp4'),
        blank=True
    ) 
    def __str__(self):
        pass

    def save(self, *args, **kwargs):
        # Calcola la durata del video solo se è impostato il video
        if self.videos:
            try:
                video_path = self.videos.path
                clip = VideoFileClip(video_path)
                self.duration = timezone.timedelta(seconds=clip.duration)
            except OSError as e:
                print(f"Errore nel caricare il video: {e}")

        super().save(*args, **kwargs)
   
    class Meta:
        verbose_name_plural = "Lezioni"

class Purchase(models.Model):    
    """
    Entity that describe the relationship between user and course and models a purchase of a course.
    """
    utente = models.ForeignKey(User, on_delete=models.PROTECT)
    corso = models.ForeignKey(Course, on_delete=models.PROTECT)
    date = models.DateTimeField()

    def purchased_by(self):
        if self.utente == None: return None
        return self.utente.username
    
    class Meta:
        verbose_name_plural = "Acquisti"
