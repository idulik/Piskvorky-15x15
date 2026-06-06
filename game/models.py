from django.db import models
from django.contrib.auth.models import User

class PlayerStats(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)

    @property
    def win_rate(self):
        total = self.wins + self.losses
        if total == 0:
            return 0
        return round((self.wins / total) * 100)

    def __str__(self):
        return self.user.username

