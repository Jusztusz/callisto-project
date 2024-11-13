from django.shortcuts import render
import psutil
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

@login_required
def network(request):
    interfaces = psutil.net_io_counters(pernic=True).keys()
    return render(request, "network/network.html", {'interfaces': interfaces})

