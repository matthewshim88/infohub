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

def index(request):
    if "userID" not in request.session:
        # Prevent user from going to the success page if not logged in.
        return redirect(reverse('useradmin:index'))

    # User is logged in.
    userID = request.session['userID']

    context = {
        "first_name" : User.objects.get(id = userID).first_name,
        "stories" : []
    }

    return render(request, 'infohub/index.html', context)

# Get the articles for the user's selected sources.
def getInfo(request):
    print "DEBUG: Entering getInfo"
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
