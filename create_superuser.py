import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "piskvorky.settings")  # uprav podľa názvu projektu
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

username = "admin"
email = "idulik@gmail.com"
password = "kitina1982x"

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(
        username=username,
        email=email,
        password=password
    )
    print("Superuser created")
else:
    print("Superuser already exists")