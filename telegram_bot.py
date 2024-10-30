import requests

TOKEN = '7871685890:AAE_9nxjhNyRoZszzKOTGlch1sljVsc4--k'
CHAT_ID = '1426057434'

def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": text}
    response = requests.post(url, data=data)
    if response.status_code == 200:
        print("Üzenet sikeresen elküldve!")
    else:
        print(f"Nem sikerült elküldeni az üzenetet: {response.status_code}, {response.text}")

send_message("Adatok")
