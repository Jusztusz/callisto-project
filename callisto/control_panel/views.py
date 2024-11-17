from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
import subprocess
import psutil

def is_script_running(script_name):
    for process in psutil.process_iter(['pid', 'name', 'cmdline']):
        cmdline = process.info.get('cmdline')
        if cmdline and script_name in cmdline:
            return True
    return False

def toggle_cm_agent(request):
    script_name = "control_panel/cm_agent.py"
    script_running = is_script_running(script_name)
    
    if script_running:
        for process in psutil.process_iter(['pid', 'name', 'cmdline']):
            if script_name in process.info['cmdline']:
                process.terminate()
                break
    else:
        subprocess.Popen(["python3", script_name])

    return JsonResponse({'script_running': not script_running})

def toggle_alert_agent(request):
    script_name = "control_panel/alert_agent.py"
    script_running = is_script_running(script_name)
    
    if script_running:
        for process in psutil.process_iter(['pid', 'name', 'cmdline']):
            if script_name in process.info['cmdline']:
                process.terminate()
                break
    else:
        subprocess.Popen(["python3", script_name])

    return JsonResponse({'script_running': not script_running})

def control_panel(request):
    cm_script_name = "control_panel/cm_agent.py"
    cm_script_running = is_script_running(cm_script_name)
    
    alert_script_name = "control_panel/alert_agent.py"
    alert_script_running = is_script_running(alert_script_name)
    
    return render(request, 'control_panel/control_panel.html', {
        'cm_script_running': cm_script_running,
        'alert_script_running': alert_script_running
    })
