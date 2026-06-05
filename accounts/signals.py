from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from game.models import PlayerStats

@receiver(post_save, sender=User)
def create_player_stats(sender, instance, created, **kwargs):
    if created:
        PlayerStats.objects.create(user=instance)