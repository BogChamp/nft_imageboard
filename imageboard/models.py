from django.conf import settings
from django.db import models
from django.utils import timezone


class Image(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images/')
    image_id = models.CharField(max_length=200)
    likes = models.IntegerField()
    public = models.BooleanField()
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.likes = 0
        self.public = True
        self.save()

    def __str__(self):
        return self.title
