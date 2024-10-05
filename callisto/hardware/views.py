from django.shortcuts import render

# Create your views here.
def hardware(request):
    return render(request, "hardware/hardware.html")