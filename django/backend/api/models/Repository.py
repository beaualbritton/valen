from django.db import models
from django.contrib.auth.models import User


class Repository(models.Model):
    owner = models.ForeignKey(User, related_name='repo_owner', on_delete=models.CASCADE)
    repo_name = models.CharField(max_length=128)
    collaborators = models.ManyToManyField(User, related_name='repo_collaborator', blank=True)
    public = models.BooleanField()
    creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=['repo_name', 'owner'])]
