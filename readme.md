# Piškvorky 20x20 – Hybrid Gaming Platform

Cross-platform hra vytvorená pomocou Django (web aplikácia), Pygame (desktop klient) a REST API synchronizácie.

---

# Cieľ projektu

Vytvoriť hybridnú hru Piškvorky 20x20, ktorá umožní:

* hrať online cez webový prehliadač,
* stiahnuť desktop verziu,
* synchronizovať výsledky cez REST API,
* zobrazovať rebríček najlepších hráčov.

---

# Celý flow systému

## A. Web vstup

1. Používateľ otvorí web.
2. Vidí:

   * názov hry: Piškvorky 20x20
   * úvodný text
   * leaderboard (TOP 10 hráčov)
   * tlačidlá Login / Register

## B. Registrácia a prihlásenie

3. Používateľ sa zaregistruje.
4. Django vytvorí účet.
5. Používateľ sa prihlási.

## C. Odomknutie hry

Po prihlásení sa zobrazí:

* hracia plocha 20x20
* leaderboard
* tlačidlo na stiahnutie desktop verzie

## D. Web hra

6. Používateľ klikne na políčko.
7. Django spracuje ťah.
8. Hracia plocha sa obnoví.
9. Kontroluje sa podmienka 5 symbolov v rade.
10. Výsledok hry sa uloží.

## E. Desktop verzia

11. Používateľ stiahne aplikáciu.
12. Hrá offline.
13. Výsledky sa ukladajú lokálne.

## F. Synchronizácia

14. Po pripojení na internet:

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
│ Game Logic                 │
│ REST API                   │
└────────────┬───────────────┘
             │
      ┌──────┴──────┐
      ▼             ▼

┌────────────────┐   ┌─────────────────┐
│ PostgreSQL     │   │ REST API Layer  │
│ alebo SQLite   │   │ /api/results/   │
└────────────────┘   └────────┬────────┘
                               │
                               ▼

                   ┌────────────────────┐
                   │   PYGAME CLIENT    │
                   │ Offline Desktop    │
                   └────────────────────┘
```

---

# Databáza

## User

* id
* username
* password

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
* board_size = 20
* moves_count
* timestamp

## OfflineQueue

* local results
* synced (true / false)

---

# Wireframe

## Hlavná stránka

```text
┌──────────────────────────────────────────────┐
│ HEADER                                       │
│ Piškvorky 20x20 | Home | Login | Register    │
└──────────────────────────────────────────────┘

┌──────────────────────────────────────────────┐
│ INTRO TEXT                                   │
│ Spoj 5 v rade na 20x20 poli                  │
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
│                20x20 GRID                    │
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

* 20x20 grid
* klikateľná mriežka
* X/O systém
* kontrola 5 v rade
* herný stav na serveri

Výsledok:

✔ Hra v prehliadači

## Fáza 4 – REST API

Endpointy:

* POST /api/results/
* GET /api/leaderboard/

Výsledok:

✔ Komunikácia klient ↔ server

## Fáza 5 – Pygame klient

* offline hra
* lokálne výsledky

Výsledok:

✔ Desktop verzia

## Fáza 6 – Synchronizácia

* kontrola internetu
* odosielanie výsledkov
* retry mechanizmus

Výsledok:

✔ Offline + online režim

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
* JavaScript
* Pygame
* SQLite
* PostgreSQL
* JSON
* REST API
* Git
* GitHub
* VS Code
