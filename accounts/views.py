# REGISTRÁCIA
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth import login
from django.shortcuts import render
from django.contrib import messages
from .forms import RegisterForm
import traceback
from game.models import PlayerStats

def register(request):
    success = False

    if request.method == "POST":
        form = RegisterForm(request.POST)

        print("POST DATA:", request.POST)

        if form.is_valid():
            print("REGISTER VALID")

            try:
                user = form.save()
                print("USER SAVED:", user.username)

                # 🔥 DÔLEŽITÉ (ak používaš leaderboard)
                PlayerStats.objects.get_or_create(
                    user=user,
                    defaults={"wins": 0, "losses": 0}
                )

                messages.success(request, "Účet bol vytvorený.")
                success = True

                # ✔ PRESMEROVANIE
                return redirect("home")

            except Exception as e:
                print("REGISTER SAVE ERROR:", repr(e))
                traceback.print_exc()

        else:
            print("REGISTER INVALID")
            print("FORM ERRORS:", form.errors.as_json())

    else:
        form = RegisterForm()

    return render(request, "register.html", {
        "form": form,
        "success": success
    })

