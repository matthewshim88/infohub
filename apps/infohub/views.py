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
import weather

def index(request):
    if "userID" not in request.session:
        # Prevent user from going to the success page if not logged in.
        return redirect(reverse('useradmin:index'))

    # User is logged in.
    userID = request.session['userID']
    # userCity = request.session['userCity']

    # Get stories from all user configured sources
    stories = sources.getInfo(userID)

    #questionable....maybe use session? Up for discussion
    current_weather = weather.getWeather(User.objects.get(id=userID).city)

    context = {
        "first_name" : User.objects.get(id = userID).first_name,
        "stories" : stories,
        "city": User.objects.get(id=userID).city,
        "weather" : current_weather
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
