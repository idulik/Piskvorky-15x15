from django.shortcuts import render

from django.shortcuts import render
from .models import PlayerStats

def leaderboard(request):
    players = PlayerStats.objects.all().order_by(
        '-wins',
        'losses'
    )[:10]

    return render(request, "leaderboard.html", {"players": players})
