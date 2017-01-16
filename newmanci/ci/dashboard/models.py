from django.db import models
from django.contrib.auth.models import User

class User(models.Model):
    user = models.OneToOneField(User)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    def __unicode__(self):
        return self.user.username

