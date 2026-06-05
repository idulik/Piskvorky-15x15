from django.shortcuts import render, redirect
from .models import PlayerStats

def leaderboard(request):
    players = PlayerStats.objects.all().order_by(
        '-wins',
        'losses'
    )[:10]

    return render(request, "leaderboard.html", {"players": players})

BOARD_SIZE = 20

# jednoduchý "fake memory" (na začiatok)
GAME_STATE = {
    "board": [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)],
    "turn": "X",
    "winner": None
}

# view pre hru
def game_view(request):
    return render(request, "game.html", GAME_STATE)

# view na ťah, každé kliknutie = request
def move(request, x, y):
    global GAME_STATE

    if GAME_STATE["winner"]:
        return redirect("game")

    if GAME_STATE["board"][x][y] is None:
        GAME_STATE["board"][x][y] = GAME_STATE["turn"]

        # switch hráča
        GAME_STATE["turn"] = "O" if GAME_STATE["turn"] == "X" else "X"

    return redirect("game")