from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def storage(request):
    return render(request, "storage/storage.html")

