Piškvorky 20x20 – Hybrid Gaming Platform (Web & Desktop Client)

Cross-platform game built with Django (web application), Pygame (desktop client) and REST API synchronization.

CELÝ FLOW SYSTÉMU
A. Web vstup
1. user otvorí web (Django)
2. vidí:
   - názov: Piškvorky 20x20
   - intro text
   - leaderboard (TOP 10 hráčov)
   - tlačidlá: Login / Register

B. Registrácia / login
3. user sa zaregistruje
4. Django vytvorí účet
5. user sa prihlási

C. Odomknutie hry
6. po login:

WEB zobrazí:
- 20x20 piškvorky (klikateľná mriežka)
- leaderboard ostáva
- tlačidlo "Stiahnuť desktop verziu"

D. Web hra (online verzia)
7. user klikne na políčko v 20x20 mriežke
8. Django spracuje ťah a obnoví stránku
9. hra kontroluje 5 v rade (X/O)
10. po skončení:
   - výsledok sa odošle na server

Po kliknutí na políčko sa odošle požiadavka na server, Django spracuje ťah, aktualizuje herný stav a znovu vykreslí hraciu plochu.

E. Desktop verzia (Pygame)
11. user si stiahne hru
12. hrá offline
13. výsledky sa ukladajú lokálne

F. Synchronizácia (REST API)
14. keď je internet:
    Pygame klient pošle výsledky na server

15. server:
    - uloží výsledky
    - aktualizuje štatistiky

G. Štatistiky (leaderboard)
16. web zobrazí TOP 10 hráčov:

Pravidlá:
- zoradenie podľa počtu výhier (DESC)
- pri rovnakom počte výhier podľa prehier (ASC)
- zobrazí sa max 10 hráčov
Zobrazované stĺpce:
- meno hráča
- výhry
- prehry
- win rate (dynamicky)

Win rate = wins / (wins + losses)

ARCHITEKTÚRA
                     ┌────────────────────────────┐
                     │        WEB BROWSER         │
                     │     HTML/CSS (frontend)    │
                     └────────────┬───────────────┘
                                  │
                                  ▼
                     ┌────────────────────────────┐
                     │        DJANGO SERVER       │
                     │----------------------------│
                     │ - login/register           │
                     │ - leaderboard              │
                     │ - web game logic (Python)  │
                     │ - REST API (DRF)           │
                     └────────────┬───────────────┘
                                  │
                 ┌────────────────┼────────────────┐
                 ▼                                 ▼
      ┌────────────────────┐         ┌────────────────────────┐
      │    DATABASE        │         │     REST API LAYER     │
      │  PostgreSQL/SQLite │         │ /api/results/          │
      └────────────────────┘         └──────────┬─────────────┘
                                                │
                                                ▼
                                ┌────────────────────────────┐
                                │     PYGAME CLIENT          │
                                │  (offline desktop game)    │
                                └────────────────────────────┘

DATABÁZA (core model)
User
- id
- username
- password

PlayerStats
- user_id
- wins
- losses

python
@property
def win_rate(self):
    total = self.wins + self.losses
    if total == 0:
        return 0
    return round((self.wins / total) * 100, 2)

GameResult
- user_id
- result (win/loss/draw)
- board_size = 20
- moves_count
- timestamp

OfflineQueue
- local results (pygame)
- synced = false/true

WIREFRAME (WEB STRÁNKA)

HLAVNÁ STRÁNKA
┌────────────────────────────────────────────────────┐
│                    HEADER                          │
│  Piškvorky 20x20 | Home | Login | Register         │
└────────────────────────────────────────────────────┘
┌────────────────────────────────────────────────────┐
│                    INTRO TEXT                      │
│  "Spoj 5 v rade na 20x20 poli!"                    │
└────────────────────────────────────────────────────┘
┌────────────────────────────────────────────────────┐
│                  LEADERBOARD                       │
│  Meno | Výhry | Prehry | Win rate                  │
│  Jana | 12    | 5      | 70%                       │
│  Peter| 8     | 7      | 53%                       │
│  Adam | 3     | 10     | 23%                       │
└────────────────────────────────────────────────────┘
┌────────────────────────────────────────────────────┐
│            IF USER NOT LOGGED IN                   │
│  Pre hranie sa musíš zaregistrovať                 │
│  [ Register ]   [ Login ]                          │
└────────────────────────────────────────────────────┘
┌────────────────────────────────────────────────────┐
│            IF USER LOGGED IN                       │
│                                                    │                                       
│ 20x20 mriežka                                      │
│  X/O striedanie                                    │
│  RULE: 5 in a row wins                             │
│  Status: Player X turn                             │
│  Po každom ťahu sa stránka automaticky obnoví.     │
│                                                    │
│  [ Restart ]                                       │
└────────────────────────────────────────────────────┘
┌────────────────────────────────────────────────────┐
│               DOWNLOAD SECTION                     │
│  "Stiahni desktop verziu (Pygame)"                 │
│  [Download .exe]                                   │
└────────────────────────────────────────────────────┘

DETAIL HRY (ZOOM)
┌────────────────────────────────────────────┐
│  PLAYER X vs PLAYER O                      │
├────────────────────────────────────────────┤
│ 20x20 grid                                 │
│ 2 hráči (X/O)                              │
│ horizontálne / vertikálne / diagonálne     │
├────────────────────────────────────────────┤
│ Status: X to play                          │
│ Rule: first 5 in a row wins                │
└────────────────────────────────────────────┘


 
IMPLEMENTAČNÝ PLÁN – PIŠKVORKY 20x20

FÁZA 1 – BACKEND (DJANGO)

•	vytvorenie projektu
•	accounts app
•	game app
•	user system (login/register)
•	PlayerStats model

✔ výsledok: funkčný backend 

FÁZA 2 – LEADERBOARD

•	TOP 10 hráčov
•	zoradenie podľa wins a losses
•	HTML tabuľka

✔ výsledok: leaderboard funguje

FÁZA 3 – WEB HRA (DJANGO)

•	20x20 grid
•	klikateľná mriežka
•	X/O systém
•	win check (5 v rade)
•	herný stav uložený na serveri
•	odosielanie ťahov pomocou Django formulárov
•	obnovenie stránky po každom ťahu
✔ výsledok: hra v browseri 
FÁZA 4 – REST API (DRF)

Endpoints:

•	POST /api/results/
•	GET /api/leaderboard/

✔ výsledok: backend komunikácia 

FÁZA 5 – PYGAME CLIENT

•	offline hra
•	20x20 grid
•	lokálne ukladanie výsledkov

✔ výsledok: desktop verzia 

FÁZA 6 – SYNCHRONIZÁCIA

•	kontrola internetu
•	odosielanie dát na API
•	retry systém

✔ výsledok: offline + online hybrid

FÁZA 7 – FINÁLNY SYSTEM
•	web login 
•	leaderboard 
•	web hra 
•	desktop hra 
•	synchronizácia dát 


TECHNOLÓGIE
•	Django 
•	Django REST Framework 
•	HTML/CSS 
•	Pygame 
•	SQLite / PostgreSQL 
•	JSON API sync
CIEĽ PROJEKTU

Hybridná hra Piškvorky 20x20 s:

•	webovou hrou implementovanou v Django (Python)
•	desktop verziou
•	synchronizáciou výsledkov
•	rebríčkom hráčov
