from django.shortcuts import render,redirect
from django.core.urlresolvers import reverse
from .models import InfoSource, Audit
from ..login_reg.models import User
from django.contrib import messages

import time
import urllib2
import json
import adminportal
import sources

def index(request):
    if "userID" not in request.session:
        # Prevent user from going to the success page if not logged in.
        return redirect(reverse('useradmin:index'))

    # User is logged in.
    userID = request.session['userID']

    # Get stories from all user configured sources
    stories = sources.getInfo(userID)
    context = {
        "first_name" : User.objects.get(id = userID).first_name,
        "stories" : stories
    }

    return render(request, 'infohub/index.html', context)

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
    currentSettings["Bing"] = { "Enabled" : ""}
    currentSettings["CNN"] = { "Enabled" : ""}
    currentSettings["NPR"] = { "Enabled" : ""}

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
        # print ("*" * 50)
        # print request.POST
        InfoSource.objects.set(request.POST, request.session["userID"])
    return redirect(reverse('info:show_profile'))
