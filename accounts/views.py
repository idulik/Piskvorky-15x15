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

        if form.is_valid():
            print("REGISTER VALID")

            try:
                user = form.save()
                print("REGISTER SAVED OK:", user)
                success = True
                form = None

                messages.success(
                    request,
                    "Vaše konto bolo úspešne vytvorené. Môžete túto stránku zavrieť a vrátiť sa na úvodnú stránku, kde sa prihlásite pod svojím menom a heslom, ktoré ste zadali."
                )

            except Exception as e:
                print("REGISTER SAVE ERROR:", e)
                traceback.print_exc()

        else:
            print("REGISTER FORM INVALID")
            print(form.errors)

    else:
        form = RegisterForm()

    return render(request, "register.html", {
        "form": form,
        "success": success
    })
