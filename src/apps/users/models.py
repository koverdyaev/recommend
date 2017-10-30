from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.db import models


class User(AbstractUser):

    tracks = models.ManyToManyField('music.Track')

    def __str__(self):
        return self.username

