import hashlib
from urllib.parse import urlencode
from django.contrib.auth.models import User
from django.db import models

class UserDetails(models.Model):
    user = models.ForeignKey(User, related_name="details", on_delete=models.CASCADE)
    about_me = models.TextField(blank=True, default="")
    
    class Meta:
        verbose_name_plural = "User Details"
    
    def __str__(self):
        return f"{self.user} details"
    
    def gravatar(self):
        email = self.user.email.lower().encode('utf-8')
        default = 'mm'
        size = 256
        url = 'https://www.gravatar.com/avatar/{md5}?{params}'.format(
            md5=hashlib.md5(email).hexdigest(),
            params=urlencode({'d': default, 's': str(size)})
        )
        return url

class Followers(models.Model):
    follower = models.ForeignKey(User, related_name="following", on_delete=models.CASCADE)
    followed = models.ForeignKey(User, related_name="followers", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ("follower_id", "followed_id",)
        verbose_name_plural = "Followers"

    def __str__(self):
        return f"{self.follower.username} -> {self.followed.username}"