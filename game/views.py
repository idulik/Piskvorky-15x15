from django.shortcuts import render, redirect
from .models import PlayerStats
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

import math

# =========================
# AUTH
# =========================

def home(request):
    form = AuthenticationForm()

    top_players = PlayerStats.objects.select_related("user").all().order_by('-wins', 'losses')[:10]
    
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")

    return render(request, "home.html", {
        "form": form,
        "top_players": top_players
    })


def logout_view(request):
    logout(request)
    return redirect("home")


def leaderboard(request):
    players = PlayerStats.objects.all().order_by('-wins', 'losses')[:10]
    return render(request, "leaderboard.html", {"players": players})


# =========================
# GAME VIEW
# =========================

@login_required
def game_view(request):

    if "board" not in request.session:
        request.session["board"] = [
            [None for _ in range(20)]
            for _ in range(20)
        ]
        request.session["winner"] = None

    return render(request, "game.html", {
        "board": request.session["board"],
        "winner": request.session["winner"],
        "last_ai_move": request.session.get("last_ai_move")
    })


# =========================
# GAME CONSTANTS
# =========================

SIZE = 20
AI = "O"
HUMAN = "X"


# =========================
# WIN CHECK
# =========================

def check_winner_simple(board, x, y, player):
    directions = [(1,0), (0,1), (1,1), (1,-1)]

    for dx, dy in directions:
        count = 1

        i = 1
        while 0 <= x + dx*i < SIZE and 0 <= y + dy*i < SIZE and board[x + dx*i][y + dy*i] == player:
            count += 1
            i += 1

        i = 1
        while 0 <= x - dx*i < SIZE and 0 <= y - dy*i < SIZE and board[x - dx*i][y - dy*i] == player:
            count += 1
            i += 1

        if count >= 5:
            return True

    return False


# =========================
# FAST MOVE GENERATOR
# =========================

def get_moves(board):

    moves = []

    center = SIZE // 2

    for x in range(SIZE):
        for y in range(SIZE):

            if board[x][y] is not None:
                continue

            found = False

            for dx in range(-3, 4):
                for dy in range(-3, 4):

                    nx = x + dx
                    ny = y + dy

                    if (
                        0 <= nx < SIZE and
                        0 <= ny < SIZE and
                        board[nx][ny] is not None
                    ):
                        found = True
                        break

                if found:
                    break

            if found:
                priority = move_priority(board, x, y)
                moves.append((-priority, x, y))

    if not moves:
        return [(center, center)]

    moves.sort()

    return [(x, y) for _, x, y in moves[:20]]


def count_line(board, x, y, dx, dy, player):

    count = 1
    open_ends = 0

    i = 1
    while (
        0 <= x + dx * i < SIZE and
        0 <= y + dy * i < SIZE and
        board[x + dx * i][y + dy * i] == player
    ):
        count += 1
        i += 1

    if (
        0 <= x + dx * i < SIZE and
        0 <= y + dy * i < SIZE and
        board[x + dx * i][y + dy * i] is None
    ):
        open_ends += 1

    i = 1
    while (
        0 <= x - dx * i < SIZE and
        0 <= y - dy * i < SIZE and
        board[x - dx * i][y - dy * i] == player
    ):
        count += 1
        i += 1

    if (
        0 <= x - dx * i < SIZE and
        0 <= y - dy * i < SIZE and
        board[x - dx * i][y - dy * i] is None
    ):
        open_ends += 1

    return count, open_ends

def evaluate_pattern(count, open_ends):

    if count >= 5:
        return 1000000

    # OPEN FOUR
    if count == 4 and open_ends == 2:
        return 500000

    # CLOSED FOUR
    if count == 4 and open_ends == 1:
        return 100000

    # OPEN THREE
    if count == 3 and open_ends == 2:
        return 5000

    # CLOSED THREE
    if count == 3 and open_ends == 1:
        return 500

    # OPEN TWO
    if count == 2 and open_ends == 2:
        return 100

    # CLOSED TWO
    if count == 2 and open_ends == 1:
        return 20

    return 0

# =========================
# EVALUATION (FAST)
# =========================

def evaluate_board(board):

    score = 0

    directions = [
        (1, 0),
        (0, 1),
        (1, 1),
        (1, -1)
    ]

    for x in range(SIZE):
        for y in range(SIZE):

            player = board[x][y]

            if player is None:
                continue

            for dx, dy in directions:

                count, open_ends = count_line(
                    board,
                    x,
                    y,
                    dx,
                    dy,
                    player
                )

                value = evaluate_pattern(
                    count,
                    open_ends
                )

                if player == AI:
                    score += value
                else:
                    score -= int(value * 1.3)

    return score

def move_priority(board, x, y):

    score = 0

    # základné skóre za okolie
    for dx in range(-2, 3):
        for dy in range(-2, 3):

            nx = x + dx
            ny = y + dy

            if 0 <= nx < SIZE and 0 <= ny < SIZE:

                if board[nx][ny] == AI:
                    score += 4

                elif board[nx][ny] == HUMAN:
                    score += 5

    # BONUS za vytvorenie vlastnej štvorky
    board[x][y] = AI

    for dx, dy in [(1,0), (0,1), (1,1), (1,-1)]:

        count, open_ends = count_line(
            board,
            x,
            y,
            dx,
            dy,
            AI
        )

        if count >= 4:
            score += 50000

    board[x][y] = None

    # BONUS za blokovanie súperovej štvorky
    board[x][y] = HUMAN

    for dx, dy in [(1,0), (0,1), (1,1), (1,-1)]:

        count, open_ends = count_line(
            board,
            x,
            y,
            dx,
            dy,
            HUMAN
        )

        if count >= 4:
            score += 100000

    board[x][y] = None

    return score

# =========================
# MINIMAX (DEPTH 3)
# =========================

def minimax(board, depth, alpha, beta, maximizing):

    if depth == 0:
        return evaluate_board(board)

    moves = get_moves(board)

    if maximizing:
        best = -math.inf

        for x, y in moves:
            board[x][y] = AI

            if check_winner_simple(board, x, y, AI):
                board[x][y] = None
                return 10000000

            val = minimax(board, depth-1, alpha, beta, False)
            board[x][y] = None

            best = max(best, val)
            alpha = max(alpha, val)

            if beta <= alpha:
                break

        return best

    else:
        best = math.inf

        for x, y in moves:
            board[x][y] = HUMAN

            if check_winner_simple(board, x, y, HUMAN):
                board[x][y] = None
                return -10000000

            val = minimax(board, depth-1, alpha, beta, True)
            board[x][y] = None

            best = min(best, val)
            beta = min(beta, val)

            if beta <= alpha:
                break

        return best


# =========================
# AI MOVE (FAST PRO)
# =========================

def ai_move(board):

    moves = get_moves(board)

    # okamžitá výhra
    for x, y in moves:

        board[x][y] = AI

        if check_winner_simple(board, x, y, AI):
            board[x][y] = None
            return (x, y)

        board[x][y] = None

    # okamžitý blok
    for x, y in moves:

        board[x][y] = HUMAN

        if check_winner_simple(board, x, y, HUMAN):
            board[x][y] = None
            return (x, y)

        board[x][y] = None

    best_score = -math.inf
    best_move = None

    for x, y in moves:

        board[x][y] = HUMAN

        threat = False

        for dx, dy in [(1,0),(0,1),(1,1),(1,-1)]:

            count, open_ends = count_line(
                board,
                x,
                y,
                dx,
                dy,
                HUMAN
            )

            if count >= 4:
                threat = True
                break

        board[x][y] = None

        if threat:
            return (x, y)
    
    # vytvor otvorenú štvorku

    for x, y in moves:

        board[x][y] = AI

        for dx, dy in [(1,0),(0,1),(1,1),(1,-1)]:

            count, open_ends = count_line(
                board,
                x,
                y,
                dx,
                dy,
                AI
            )

            if count == 4 and open_ends >= 1:
                board[x][y] = None
                return (x, y)

        board[x][y] = None

    # blokuj súperovu štvorku

    for x, y in moves:

        board[x][y] = HUMAN

        for dx, dy in [(1,0),(0,1),(1,1),(1,-1)]:

            count, open_ends = count_line(
                board,
                x,
                y,
                dx,
                dy,
                HUMAN
            )

            if count == 4 and open_ends >= 1:
                board[x][y] = None
                return (x, y)

        board[x][y] = None

    for x, y in moves:

        board[x][y] = AI

        score = minimax(
            board,
            2,
            -math.inf,
            math.inf,
            False
        )

        board[x][y] = None

        if score > best_score:
            best_score = score
            best_move = (x, y)

    return best_move


# =========================
# MOVE VIEW
# =========================

def move(request, x, y):

    board = request.session.get("board")
    winner = request.session.get("winner")
    if board is None:
        return redirect("game")

    if winner:
        return redirect("game")

    if board[x][y] is None:
        board[x][y] = HUMAN

        if check_winner_simple(board, x, y, HUMAN):
            request.session["winner"] = "X"

            if request.user.is_authenticated:
                stats, created = PlayerStats.objects.get_or_create(
                    user=request.user
                )
                stats.wins += 1
                stats.save()

            request.session["board"] = board
            return redirect("game")

        # AI move
        ai_pos = ai_move(board)

        if ai_pos:
            ax, ay = ai_pos
            board[ax][ay] = AI

            request.session["last_ai_move"] = (ax, ay)

            if check_winner_simple(board, ax, ay, AI):
                request.session["winner"] = "O"

                if request.user.is_authenticated:
                    stats, created = PlayerStats.objects.get_or_create(
                        user=request.user
                    ) 
                    stats.losses += 1
                    stats.save()

    request.session["board"] = board
    request.session.modified = True

    return redirect("game")


# =========================
# RESET
# =========================

def reset(request):
    request.session["board"] = [
        [None for _ in range(20)] for _ in range(20)
    ]
    request.session["winner"] = None
    request.session["last_ai_move"] = None
    request.session.modified = True

    source = request.GET.get("from")

    if source == "home":
        return redirect("home")

    return redirect("game")