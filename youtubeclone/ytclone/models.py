from django.db import models

# Create your models here.

class Video(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    upload_date = models.DateTimeField(auto_now_add=True)
    video_url = models.URLField(max_length=200)
    thumbnail_url = models.URLField(max_length=200)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title