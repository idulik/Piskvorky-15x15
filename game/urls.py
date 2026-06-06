from django.urls import path
from .views import leaderboard, game_view, move, reset

urlpatterns = [
    path("leaderboard/", leaderboard, name="leaderboard"),
    path("", views.home, name="home"),

# hra
    path("", game_view, name="game"),
    path("move/<int:x>/<int:y>/", move, name="move"),
    path("reset/", reset, name="reset"),
]