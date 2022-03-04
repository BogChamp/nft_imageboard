import imagehash
from django.conf import settings
from django.db import models
from django.utils import timezone
from PIL import Image as Image_hash


class Image(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images/')
    token = models.CharField(max_length=200)
    likes = models.IntegerField(default=0)
    public = models.BooleanField()
    date_last_own = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.date_last_own = timezone.now()
        self.likes = 0
        self.public = True
        image_hash_obj = Image_hash.open(self.image)
        self.token = imagehash.average_hash(image_hash_obj)
        History.objects.create(
            owner=self.owner,
            image=self,
            date=self.date_last_own
        )
        self.save()

    def __str__(self):
        return self.title


class History(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user) + ':' + str(self.image.token) + ':' + str(
            self.date)


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
