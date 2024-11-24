import os
import random
import string

# Véletlenszerű string generálása
def generate_secret_key(length=50):
    chars = string.ascii_letters + string.digits + string.punctuation
    secret_key = ''.join(random.choice(chars) for _ in range(length))
    return secret_key

# Titkos kulcs létrehozása
secret_key = generate_secret_key()

# .env fájl létrehozása és írása
env_file_path = '/app/callisto-project/callisto/callisto/.env'
with open(env_file_path, 'w') as f:
    f.write(f"SECRET_KEY='{secret_key}'\n")
    f.write("DB_NAME='postgres'\n")
    f.write("DB_USER='postgres'\n")
    f.write("DB_PASSWORD='PSQ**1'\n")
    f.write("DB_HOST='127.0.0.1'\n")
    f.write("DB_PORT='6969'\n")

print(f".env file created with SECRET_KEY: {secret_key}")