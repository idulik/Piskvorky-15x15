# Piškvorky 15x15 – Hybrid Gaming Platform

Cross-platform hra vytvorená pomocou Django (web aplikácia), Pygame (desktop klient) a REST API synchronizácie.

---

# Cieľ projektu

Cieľom projektu je vytvoriť jednoduchú single-player hru Piškvorky 15x15, kde hráč hrá proti počítaču (AI). Hra bude dostupná ako webová aplikácia a desktop verzia, pričom výsledky sa budú synchronizovať na server.

---

# Celý flow systému

## A. Web vstup

1. Používateľ otvorí web.
2. Vidí:

   * názov hry: Piškvorky 15x15
   * úvodný text
   * leaderboard (TOP 10 hráčov)
   * tlačidlá Login / Register

## B. Registrácia a prihlásenie

3. Používateľ sa zaregistruje.
4. Django vytvorí účet.
5. Používateľ sa prihlási.

## C. Odomknutie hry

Po prihlásení sa zobrazí:

* hracia plocha 15x15
* leaderboard
* tlačidlo na stiahnutie desktop verzie

## D. Web hra

6. Používateľ klikne na políčko.
7. Django spracuje ťah hráča.
8. Ak hra neskončila, automaticky vykoná ťah počítač (AI).
9. Hracia plocha sa obnoví.
10. Kontroluje sa podmienka 5 symbolov v rade.
11. Výsledok hry sa uloží.

## E. Desktop verzia

12. Používateľ stiahne aplikáciu.
13. Hrá offline.
14. Výsledky sa ukladajú lokálne.

## F. Synchronizácia

15. Po pripojení na internet:

* desktop klient odošle výsledky na server,
* server aktualizuje štatistiky.

## G. Leaderboard

Pravidlá:

* zoradenie podľa počtu výhier (DESC)
* pri rovnosti výhier podľa počtu prehier (ASC)
* zobrazuje sa maximálne 10 hráčov

Zobrazované stĺpce:

* meno hráča
* výhry
* prehry
* win rate

Win rate:

wins / (wins + losses)

## H. AI systém (web aj desktop)
AI hrá náhodne / alebo podľa jednoduchých pravidiel:
* blokuje 4 v rade
* preferuje víťazný ťah
* inak random

---

# Architektúra

```text
┌────────────────────────────┐
│        WEB BROWSER         │
│      HTML / CSS UI         │
└────────────┬───────────────┘
             │
             ▼
┌────────────────────────────┐
│       DJANGO SERVER        │
│----------------------------│
│ Login / Register           │
│ Leaderboard                │
│ Game Logic (PvE vs AI)     │
│ REST API (results sync)    │
└────────────┬───────────────┘
             │
             ▼
┌────────────────────────────┐
│     SQLITE / POSTGRESQL    │
└────────────────────────────┘

(optional)
┌────────────────────────────┐
│      PYGAME CLIENT         │
│   Offline single-player    │
│ Local result storage       │
│ Sync via REST API          │
└────────────────────────────┘
```

---

# Databáza

## User

* id
* username
* password (hashed via Django auth system)

## PlayerStats

* user_id
* wins
* losses

```python
@property
def win_rate(self):
    total = self.wins + self.losses

    if total == 0:
        return 0

    return round((self.wins / total) * 100, 2)
```

## GameResult

* user_id
* result
* board_size = 15
* moves_count
* timestamp

---

# Wireframe

## Hlavná stránka

```text
┌──────────────────────────────────────────────┐
│ HEADER                                       │
│ Piškvorky 15x15 | Home | Login | Register    │
└──────────────────────────────────────────────┘

┌──────────────────────────────────────────────┐
│ INTRO TEXT                                   │
│ Spoj 5 v rade na 15x15 poli                  │
└──────────────────────────────────────────────┘

┌──────────────────────────────────────────────┐
│ LEADERBOARD                                  │
│ Meno | Výhry | Prehry | Win rate             │
└──────────────────────────────────────────────┘

┌──────────────────────────────────────────────┐
│ IF USER NOT LOGGED IN                        │
│ Pre hranie sa musíš zaregistrovať            │
│ [ Register ] [ Login ]                       │
└──────────────────────────────────────────────┘

┌──────────────────────────────────────────────┐
│ IF USER LOGGED IN                            │
│                                              │
│                15x15 GRID                    │
│                                              │
│ Status: Player X turn                        │
│ Rule: 5 in a row wins                        │
│                                              │
│ [ Restart ]                                  │
└──────────────────────────────────────────────┘

┌──────────────────────────────────────────────┐
│ DOWNLOAD SECTION                             │
│ Stiahni desktop verziu                       │
│ [ Download .exe ]                            │
└──────────────────────────────────────────────┘
```

---

# Implementačný plán

## Fáza 1 – Backend

* Django projekt
* Accounts app
* Game app
* Login
* Registrácia
* PlayerStats model

Výsledok:

✔ Funkčný backend

## Fáza 2 – Leaderboard

* TOP 10 hráčov
* Zoradenie podľa výhier
* HTML tabuľka

Výsledok:

✔ Funkčný leaderboard

## Fáza 3 – Web hra

* 15x15 grid
* klikateľná mriežka
* X/O systém
* kontrola 5 v rade
* herný stav na serveri

Výsledok:

✔ Hra v prehliadači

## Fáza 4 – REST API

Endpointy:

* POST /api/results/
→ uloží výsledok hry (win/loss/draw)

* GET /api/leaderboard/
→ vracia TOP 10 hráčov

* POST /api/sync/
→ sync desktop výsledkov (voliteľné)

Výsledok:

✔ Komunikácia klient ↔ server

## Fáza 5 – PC verzia

* offline desktop verzia hry (Pygame client)

## Fáza 6 – Synchronizácia

* desktop klient odošle uložené výsledky na server
* server aktualizuje PlayerStats
* implementácia REST API komunikácie

Výsledok:

✔ offline + online sync výsledkov

## Fáza 7 – Finálny systém

* web hra
* desktop hra
* leaderboard
* synchronizácia

Výsledok:

✔ Kompletná hybridná platforma

---

# Použité technológie

* Python
* Django
* Django REST Framework
* HTML
* CSS
* Pygame
* SQLite
* PostgreSQL
* JSON
* HTTP / REST API
* Git
* GitHub
* VS Code
