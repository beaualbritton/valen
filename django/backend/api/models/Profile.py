from django.db import models
from django.contrib.auth.models import User


# Later functionality for profile pictures
def profile_path(this, filename):
    return f"profile_images/user_{this.user.id}/{filename}"

# NOT CURRENTLY IN USE!
class Profile(models.Model):
    # Every Profile has a User
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.CharField(blank=True)
    # ImageField (stored as a filepath).
    picture = models.ImageField(upload_to='api.models.profile_path', blank=True)
    # A Profile can have many Profiles following it. 
    # Relating followers to following
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following')
    # A Profile can have Many favorites

    # Follow functionality that can be called on a Profile object
    def follow(self, profile):
        if profile != self:
            self.followers.add(profile)

    def unfollow(self, profile):
        if profile != self:
            self.followers.remove(profile)
