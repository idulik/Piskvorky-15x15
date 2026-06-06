# REGISTRÁCIA
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth import login
from django.shortcuts import render
from django.contrib import messages
from .forms import RegisterForm
import traceback

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

                messages.success(request, "Účet bol vytvorený.")
                success = True

            except Exception as e:
                print("REGISTER SAVE ERROR:", e)
                traceback.print_exc()

        else:
            print("REGISTER INVALID")
            print(form.errors)

    else:
        form = RegisterForm()

    return render(request, "register.html", {
        "form": form,
        "success": success
    })
