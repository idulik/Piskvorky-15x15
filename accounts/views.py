# REGISTRÁCIA
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("game")
    else:
        form = UserCreationForm()

    return render(request, "register.html", {"form": form})


# Create your views here.
