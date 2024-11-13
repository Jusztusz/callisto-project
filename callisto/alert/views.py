from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import savedAlert, TelegramCredentials
import hashlib
import os
from pathlib import Path
from cryptography.fernet import Fernet
import base64
from django.contrib.auth.decorators import login_required

BASE_DIR = Path(__file__).resolve().parent.parent
BOTS_DIR = BASE_DIR / 'bots'

def save_telegram_credentials(api_key, chat_id):
    encrypted_api_key = TelegramCredentials.encrypt_api_key(api_key)
    credentials = TelegramCredentials(encrypted_api_key=encrypted_api_key, chat_id=chat_id)
    credentials.save()

    
    return {
        "message": "Telegram Bot adatok sikeresen mentve!",
        "telegram": {
            "chat_id": credentials.chat_id,
            "api_key_encrypted": credentials.encrypted_api_key,
        }
    }

def save_alert(name, component, alert_value, chatID, alertMessage):
    new_alert = savedAlert(name=name, component=component, alert_value=alert_value, chatID=chatID, alertMessage=alertMessage)
    new_alert.save()

    file_creation_response = create_alert_file(name, chatID, alertMessage)

    return {
        "message": "Sikeres mentés!",
        "alert": {
            "id": new_alert.id,  # Az ID itt van hozzáadva
            "name": new_alert.name,
            "component": new_alert.component,
            "alert_value": new_alert.alert_value,
            "chatID": new_alert.chatID,
            "alertMessage": new_alert.alertMessage,
        },
    }

@login_required
def alert(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Ha Telegram hitelesítési adatokat küldtek
        api_key = request.POST.get('api_key')
        chat_id = request.POST.get('chat_id')
        
        if api_key and chat_id:
            response_data = save_telegram_credentials(api_key, chat_id)
            return JsonResponse(response_data)

        # Értesítés mentése, ha csak az értesítés adatait küldték
        name = request.POST.get('alert-name')
        component = request.POST.get('component')
        alert_value = request.POST.get('alert-value')
        chatID = request.POST.get('receiverChatID')
        alertMessage = request.POST.get('alertMessage')

        if name and component and alert_value and chatID and alertMessage:
            response_data = save_alert(name, component, alert_value, chatID, alertMessage)
            return JsonResponse(response_data)

    # Összes értesítés lekérdezése és renderelése
    alerts = savedAlert.objects.all()
    chat_ids = TelegramCredentials.objects.values_list('chat_id', flat=True)
    credentials = TelegramCredentials.objects.all()
    return render(request, "alert/alert.html", {'alerts': alerts, 'chat_ids': chat_ids, 'credentials': credentials})

def delete_alert(request, alert_id):
    if request.method == "POST" and request.headers.get("X-Requested-With") == "XMLHttpRequest":
        alert = get_object_or_404(savedAlert, id=alert_id)
        alert.delete()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)

def delete_credential(request, chat_id):
    if request.method == "POST" and request.headers.get("X-Requested-With") == "XMLHttpRequest":
        credentials = get_object_or_404(TelegramCredentials, chat_id=chat_id)
        credentials.delete()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)

def get_telegram_credentials(request):
    if request.method == 'GET':
        try:
            credentials = list(TelegramCredentials.objects.values('chat_id', 'encrypted_api_key'))
            return JsonResponse(credentials, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    
def create_alert_file(name, chat_id, alertMessage):
    credentials = TelegramCredentials.objects.first()
    savedalert  = savedAlert.objects.first()
    
    if credentials:
        token = TelegramCredentials.decrypt_api_key(credentials.encrypted_api_key)
        chat_id = credentials.chat_id
        botname = savedalert.name

        content = f"""import requests

TOKEN = '{token}'
CHAT_ID = '{chat_id}'

def send_message(text):
    url = f"https://api.telegram.org/bot{{TOKEN}}/sendMessage"
    data = {{"chat_id": CHAT_ID, "text": text}}
    response = requests.post(url, data=data)
    if response.status_code == 200:
        print("Üzenet sikeresen elküldve!")
    else:
        print(f"Nem sikerült elküldeni az üzenetet: {{response.status_code}}, {{response.text}}")

send_message("{alertMessage}")
        """

        file_path = BOTS_DIR / f"{botname}.py"  
        with open(file_path, "w") as file:
            file.write(content)
        os.chmod(file_path, 0o764)
        return {"success": True, "message": "Fájl sikeresen létrehozva."}
    else:
        return {"success": False, "error": "Nincs mentett Telegram hitelesítő adat."}