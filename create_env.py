import os
from django.core.management.utils import get_random_secret_key

def generate_env_file():
    # Titkos kulcs generálása
    secret_key = get_random_secret_key()

    # A kívánt változók értékei
    env_vars = {
        "DJANGO_SECRET_KEY": f"'{secret_key}'",
        "DB_NAME": "'postgres'",
        "DB_USER": "'postgres'",
        "DB_PASSWORD": "'PSQ**1'",
        "DB_HOST": "'127.0.0.1'",
        "DB_PORT": "'5432'",
    }

    # A .env fájl elérési útja
    env_file_path = "/app/callisto-project/callisto/callisto/.env"
    
    # A .env fájl létrehozása vagy felülírása
    with open(env_file_path, "w") as f:
        for key, value in env_vars.items():
            f.write(f"{key}={value}\n")

    print(f".env file generated at {env_file_path}")

# Script futtatása
if __name__ == "__main__":
    generate_env_file()