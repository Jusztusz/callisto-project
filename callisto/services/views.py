from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def services(request):
    return render(request, "services/services.html")