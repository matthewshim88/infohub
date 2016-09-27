from django.shortcuts import render,redirect
from django.core.urlresolvers import reverse
from .models import InfoSource, Audit
from ..login_reg.models import User
from django.contrib import messages
import time

def index(request):
    if "userID" not in request.session:
        # Prevent user from going to the success page if not logged in.
        return redirect(reverse('useradmin:index'))

    # User is logged in.
    userID = request.session['userID']
    context = {
        "first_name" : User.objects.get(id = userID).first_name
    }
    return render(request, 'infohub/index.html', context)


########## Tests ##########

def runTests(request):
    user_id = request.session["userID"]
    test_results = []
    data = {
        "source_type": "api",
        "location" : "Bing",
        "highlight_text" : "Trump"
    }

    # Add a source
    time_start = time.time()
    result = InfoSource.objects.add(data, user_id)
    seconds = int(time.time() - time_start)
    if result.source_type == "api" and result.location == "Bing" and result.highlight_text == "Trump":
        status = "passed"
    else:
        status = "failed"

    test_results.append({
        "name" : "AddSource",
        "status" : status,
        "run_time" : str(seconds)
    })

    # Update a source
    data = {
        "source_type": "url",
        "location" : "www.msnbc.com/news",
        "highlight_text" : "Hillary",
        "source_id" : result.id
    }
    time_start = time.time()
    result = InfoSource.objects.update(data, user_id)
    seconds = int(time.time() - time_start)
    if result.source_type == "url" and result.location == "www.msnbc.com/news" and result.highlight_text == "Hillary":
        status = "passed"
    else:
        status = "failed"

    test_results.append({
        "name" : "UpdateSource",
        "status" : status,
        "run_time" : str(seconds)
    })

    # Get all sources for logged in user.
    time_start = time.time()
    result = InfoSource.objects.getActive(user_id)
    seconds = int(time.time() - time_start)
    if len(result) > 0:
        status = "passed"
    else:
        status = "failed"

    test_results.append({
        "name" : "InfoSource:getActive",
        "status" : status,
        "run_time" : str(seconds)
    })

    # Remove a source
    time_start = time.time()
    InfoSource.objects.remove(data, user_id)
    seconds = int(time.time() - time_start)
    if len(InfoSource.objects.filter(id = data["source_id"])) == 0:
        status = "passed"
    else:
        status = "failed"

    test_results.append({
        "name" : "RemoveSource",
        "status" : status,
        "run_time" : str(seconds)
    })

    # Get audit trail
    Audit.objects.audit(user_id, "Ran tests")
    MAX_AUDIT_ROWS = 20
    context = {
        "test_results" : test_results,
        "audits" : Audit.objects.getAll(MAX_AUDIT_ROWS)
    }
    return render(request, 'infohub/runtests.html', context)
