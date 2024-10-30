# views.py
from django.http import JsonResponse
from django.shortcuts import render
from .models import savedAlert

def alert(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        name = request.POST.get('alert-name')
        component = request.POST.get('component')
        alert_value = request.POST.get('alert-value')

        # Új értesítés mentése
        new_alert = savedAlert(name=name, component=component, alert_value=alert_value)
        new_alert.save()

        return JsonResponse({"message": "Sikeres mentés!"})

    return render(request, "alert/alert.html")
