from django.db import models
from django.conf import settings


class Team(models.Model):
    name = models.CharField(max_length=50)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL)

    def __str__(self):
        return self.name
