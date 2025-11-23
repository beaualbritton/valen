from django.db import models
from django.contrib.auth.models import User


class Repository(models.Model):
    owner = models.ForeignKey(User, related_name='owner', on_delete=models.CASCADE)
    repo_name = models.CharField(max_length=128)
    # TODO: fix
    #collaborators = models.ManyToManyField(User, related_name='collaborator', blank=True)
    public = models.BooleanField()
    creation = models.DateTimeField(auto_now_add=True)
