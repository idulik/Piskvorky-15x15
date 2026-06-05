from django.shortcuts import render, redirect
from .models import PlayerStats

def leaderboard(request):
    players = PlayerStats.objects.all().order_by(
        '-wins',
        'losses'
    )[:10]

    return render(request, "leaderboard.html", {"players": players})

BOARD_SIZE = 20

# view pre hru
def game_view(request):

    if "board" not in request.session:
        request.session["board"] = [
            [None for _ in range(20)]
            for _ in range(20)
        ]
        request.session["turn"] = "X"
        request.session["winner"] = None

    return render(request, "game.html", {
        "board": request.session["board"],
        "turn": request.session["turn"],
        "winner": request.session["winner"],
    })

    return render(request, "game.html", context)

# pridanie AI
import random
def get_empty_cells(board):
    cells = []
    for x in range(20):
        for y in range(20):
            if board[x][y] is None:
                cells.append((x, y))
    return cells

def score_position(board, x, y, player):
    directions = [(1,0), (0,1), (1,1), (1,-1)]
    score = 0

    opponent = "X" if player == "O" else "O"

    for dx, dy in directions:

        count_player = 0
        count_opponent = 0

        for i in range(-4, 5):
            nx, ny = x + dx*i, y + dy*i

            if 0 <= nx < 20 and 0 <= ny < 20:
                if board[nx][ny] == player:
                    count_player += 1
                elif board[nx][ny] == opponent:
                    count_opponent += 1

        # vlastné línie sú dôležité
        if count_player == 2:
            score += 10
        elif count_player == 3:
            score += 50
        elif count_player == 4:
            score += 200

        # blokovanie hráča je ešte dôležitejšie
        if count_opponent == 2:
            score += 15
        elif count_opponent == 3:
            score += 80
        elif count_opponent == 4:
            score += 300

    # bonus za stred (strategia)
    center = 10
    score += 20 - (abs(x - center) + abs(y - center))

    return score

def ai_move(board):

    empty = get_empty_cells(board)

    if not empty:
        return None

    best_score = -1
    best_move = None

    for x, y in empty:
        score = score_position(board, x, y, "O")

        if score > best_score:
            best_score = score
            best_move = (x, y)

    return best_move

    # 1. random ťah (default)
    return random.choice(empty)

def check_winner_simple(board, x, y, player):
    directions = [
        (1, 0),   # vertikálne
        (0, 1),   # horizontálne
        (1, 1),   # diagonála \
        (1, -1),  # diagonála /
    ]

    size = len(board)

    for dx, dy in directions:
        count = 1

        # dopredu
        i = 1
        while True:
            nx, ny = x + dx * i, y + dy * i
            if 0 <= nx < size and 0 <= ny < size and board[nx][ny] == player:
                count += 1
                i += 1
            else:
                break

        # dozadu
        i = 1
        while True:
            nx, ny = x - dx * i, y - dy * i
            if 0 <= nx < size and 0 <= ny < size and board[nx][ny] == player:
                count += 1
                i += 1
            else:
                break

        if count >= 5:
            return True

    return False

# view na ťah, každé kliknutie = request
def move(request, x, y):

    board = request.session.get("board")
    turn = request.session.get("turn")
    winner = request.session.get("winner")

    if winner:
        return redirect("game")

    if board[x][y] is None:
        board[x][y] = "X"

        # CHECK PLAYER WIN
        if check_winner_simple(board, x, y, "X"):
            winner = "X"

        else:
            # AI MOVE
            ai_pos = ai_move(board)

            if ai_pos:
                ax, ay = ai_pos
                board[ax][ay] = "O"

                # CHECK AI WIN
                if check_winner_simple(board, x, y, turn):
                    winner = turn

    request.session["board"] = board
    request.session["turn"] = turn
    request.session["winner"] = winner

    request.session.modified = True

    return redirect("game")

def check_winner(board, x, y, player):
    # jednoduchá verzia (horizont + vertikál + diagonály)
    directions = [(1,0), (0,1), (1,1), (1,-1)]

    for dx, dy in directions:
        count = 1

        # dopredu
        i = 1
        while True:
            nx, ny = x + dx*i, y + dy*i
            if 0 <= nx < 20 and 0 <= ny < 20 and board[nx][ny] == player:
                count += 1
                i += 1
            else:
                break

        # dozadu
        i = 1
        while True:
            nx, ny = x - dx*i, y - dy*i
            if 0 <= nx < 20 and 0 <= ny < 20 and board[nx][ny] == player:
                count += 1
                i += 1
            else:
                break

        if count >= 5:
            return player

    return None

def reset(request):
    request.session["board"] = [
        [None for _ in range(20)] for _ in range(20)
    ]
    request.session["turn"] = "X"
    request.session["winner"] = None

    request.session.modified = True
    return redirect("game")