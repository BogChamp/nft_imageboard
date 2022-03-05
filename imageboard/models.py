import imagehash
from django.conf import settings
from django.db import models
from django.utils import timezone
from PIL import Image as Image_hash


class Image(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images/')
    token = models.CharField(max_length=200)
    secret = models.CharField(blank=False, max_length=64)  #TODO collisions
    likes = models.IntegerField(default=0)
    public = models.BooleanField()
    date_last_own = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.date_last_own = timezone.now()
        self.likes = 0
        self.public = True
        image_hash_obj = Image_hash.open(self.image)
        self.token = imagehash.average_hash(image_hash_obj)
        if Image.objects.filter(token=self.token).exists():
            return False
        else:
            self.save()
            history_log = History.objects.create(
                owner=self.owner,
                image=self,
                date=self.date_last_own
            )
            history_log.save()
            return True

    def recover(self, secret_hash):
        print(f'model.py: {secret_hash}')
        if Image.objects.filter(secret=secret_hash).exists():
            return True
        else:
            return False

    def __str__(self):
        return self.title


class History(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.owner) + ' : ' + str(self.date)


class Preference(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user) + ':' + str(self.date)

    class Meta:
        unique_together = ("user", "image")

class UserInfo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    name = models.CharField(max_length=20, blank=True)
    second_name = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(blank=True)
    info = models.CharField(max_length=500, blank=True)
