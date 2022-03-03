from django.conf import settings
from django.db import models
from django.utils import timezone
import hashlib


class Image(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images/')
    token = models.CharField(max_length=200)
    likes = models.IntegerField(default=0)
    public = models.BooleanField()
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.likes = 0
        self.public = True
        self.token = hashlib.sha1(self.image).hexdigest()
        self.save()

    def __str__(self):
        return self.title


# class History

class Preference(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user) + ':' + str(self.image.token) + ':' + str(
            self.date)

    class Meta:
        unique_together = ("user", "image")
