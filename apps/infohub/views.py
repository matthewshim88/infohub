from django.shortcuts import render,redirect
from django.core.urlresolvers import reverse
from .models import InfoSource, Audit
from ..login_reg.models import User
from django.contrib import messages
from django.http import HttpResponse

import time
import urllib2
import json
import adminportal
import sources
import weather

def index(request):
    if "userID" not in request.session:
        # Prevent user from going to the success page if not logged in.
        return redirect(reverse('useradmin:index'))

    # User is logged in.
    userID = request.session['userID']
    # userCity = request.session['userCity']

    #questionable....maybe use session? Up for discussion
    current_weather = {}
    try:
        current_weather = weather.getWeather(User.objects.get(id=userID).city)
    except Exception as e:
        # This might fail due to an API key issue.
        # Ignoring errors for now.
        pass;

    context = {
        "first_name" : User.objects.get(id = userID).first_name,
        "stories" : [],
        "city": User.objects.get(id=userID).city,
        "weather_status" : current_weather[2],
        "weather_temp" : current_weather[3],
        "weather_humidity" : current_weather[4],
        "coords" : [current_weather[5], current_weather[6]]
    }

    return render(request, 'infohub/index.html', context)

# Gets the articles for the user's selected sources.
def getInfo(request):
    if "userID" not in request.session:
        # Prevent user from going to the success page if not logged in.
        return redirect(reverse('useradmin:index'))

    user_id = request.session['userID']
    stories = sources.getInfo(user_id)
    context = {
        "first_name" : user_id,
        "stories" : stories
    }
    return HttpResponse(json.dumps(stories), content_type = "application/json")

# Runs unit tests and retrieves audit history for the admin portal.
def adminPortal(request):
    user_id = request.session['userID']
    context = {
        "test_results" : adminportal.runTests(user_id),
        "audits" : adminportal.getAuditHistory(user_id)
    }
    return render(request, 'infohub/runtests.html', context)

def show_profile(request):
    user_id = request.session['userID']
    currentSettings = {}
    currentSettings["Bing"] = { "Enabled" : "" }
    currentSettings["CNN"] = { "Enabled" : "" }
    currentSettings["NPR"] = { "Enabled" : "" }

    settings = InfoSource.objects.getActive(user_id)
    for setting in settings:
        currentSettings[setting.location] = {
            "Enabled": "checked",
            "highlight_text" : setting.highlight_text
        }

    context = {
        "user": User.objects.get(id=user_id),
        "settings": currentSettings
    }
    return render(request, 'infohub/profile.html', context)

def set_preferences(request):
    if request.method == "POST" and "userID" in request.session:
        InfoSource.objects.set(request.POST, request.session["userID"])
    return redirect(reverse('info:index'))
