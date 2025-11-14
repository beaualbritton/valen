from django.db import models
from django.contrib.auth.models import User


class Token(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField()
    hash = models.CharField(max_length=255)
    creation = models.DateTimeField()
    expiration = models.DateTimeField()
