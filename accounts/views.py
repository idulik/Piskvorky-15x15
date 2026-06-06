# REGISTRÁCIA
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth import login
from django.shortcuts import render
from django.contrib import messages
from .forms import RegisterForm
import traceback

def register(request):
    success = False
    form = RegisterForm()

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            try:
                user = form.save()
                print("REGISTER OK:", user)

                messages.success(
                    request,
                    "Účet bol vytvorený."
                )

                success = True
                form = None

            except Exception as e:
                print("REGISTER ERROR:", e)
                traceback.print_exc()
        else:
            print("FORM ERRORS:", form.errors)

    return render(request, "register.html", {
        "form": form,
        "success": success
    })
