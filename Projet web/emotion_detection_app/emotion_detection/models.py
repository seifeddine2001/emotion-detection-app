

from django.db import models

class Emotion(models.Model):
    image = models.ImageField(upload_to='images/')
    predicted_emotion = models.CharField(max_length=50)
