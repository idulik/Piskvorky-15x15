# REGISTRÁCIA
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth import login
from django.shortcuts import render
from django.contrib import messages
from .forms import RegisterForm

def register(request):
    success = False

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Vaše konto bolo úspešne vytvorené. Môžete túto stránku zavrieť a vrátiť sa na úvodnú stránku, kde sa prihlásite pod svojím menom a heslom, ktoré ste zadali."
            )

            success = True
            form = None  # skryjem formulár
    else:
        form = RegisterForm()

    return render(request, "register.html", {
        "form": form,
        "success": success
    })
