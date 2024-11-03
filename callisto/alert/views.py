from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import savedAlert, TelegramCredentials
import hashlib

def save_telegram_credentials(api_key, chat_id):
    hashed_api_key = hashlib.sha256(api_key.encode()).hexdigest()
    credentials = TelegramCredentials(api_key=hashed_api_key, chat_id=chat_id)
    credentials.save()
    return {
        "message": "Telegram Bot adatok sikeresen mentve!",
        "telegram": {
            "chat_id": credentials.chat_id,
            "api_key_hashed": credentials.api_key,
        }
    }

def save_alert(name, component, alert_value, chatID):
    new_alert = savedAlert(name=name, component=component, alert_value=alert_value, chatID=chatID)
    new_alert.save()
    return {
        "message": "Sikeres mentés!",
        "alert": {
            "id": new_alert.id,  # Az ID itt van hozzáadva
            "name": new_alert.name,
            "component": new_alert.component,
            "alert_value": new_alert.alert_value,
            "chatID": new_alert.chatID,
        }
    }

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

        if name and component and alert_value and chatID:
            response_data = save_alert(name, component, alert_value, chatID)
            return JsonResponse(response_data)

    # Összes értesítés lekérdezése és renderelése
    alerts = savedAlert.objects.all()
    chat_ids = TelegramCredentials.objects.values_list('chat_id', flat=True)
    credentials = TelegramCredentials.objects.all()  # Lekérjük az összes botot
    return render(request, "alert/alert.html", {'alerts': alerts, 'chat_ids': chat_ids, 'credentials': credentials})

def delete_alert(request, alert_id):
    if request.method == "POST" and request.headers.get("X-Requested-With") == "XMLHttpRequest":
        alert = get_object_or_404(savedAlert, id=alert_id)
        alert.delete()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)

def delete_credential(request, chat_id):
    if request.method == "POST" and request.headers.get("X-Requested-With") == "XMLHttpRequest":
        credential = get_object_or_404(TelegramCredentials, chat_id=chat_id)
        credential.delete()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)

def get_telegram_credentials(request):
    if request.method == 'GET':
        credentials = TelegramCredentials.objects.values('chat_id', 'api_key')  # Válaszd ki a szükséges mezőket
        return JsonResponse(list(credentials), safe=False) 