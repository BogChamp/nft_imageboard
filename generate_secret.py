from django.core.management.utils import get_random_secret_key  

secret_key = get_random_secret_key()

file = open(".env","w")
print(f"SECRET_KEY = {secret_key}", file=file)
print("DEBUG = False", file=file)
file.close()