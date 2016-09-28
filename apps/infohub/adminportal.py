from .models import InfoSource, Audit
from ..login_reg.models import User
import time
import urllib2
import json
import sources

####################################################
#                                                  #
# This file should only contain methods used to by #
# the InfoHub admin portal.                        #
#                                                  #
####################################################

# Gets the last x number of audit entries.
def getAuditHistory(user_id):
    # Get audit trail
    Audit.objects.audit(user_id, "Ran tests")
    MAX_AUDIT_ROWS = 20
    return Audit.objects.getAll(MAX_AUDIT_ROWS)

# Runs unit tests.
def runTests(user_id):
    test_results = []
    data = {
        "source_type": "api",
        "location" : "Bing",
        "highlight_text" : "Trump"
    }

    # Add an info source
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

    # Update an info source
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

    # Get all info sources for logged in user.
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

    # Remove an info source
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

    # Retrieve data from Bing News.
    time_start = time.time()
    result_ex = sources.getInfoBing(user_id, 5, "placeholder")
    seconds = int(time.time() - time_start)
    if validResultEx(result_ex):
        status = "passed"
    else:
        status = "<span class='error_text'>failed</span>"

    test_results.append({
        "name" : "getInfoBing",
        "status" : status,
        "run_time" : str(seconds)
    })

    # Retrieve data from CNN.
    time_start = time.time()
    result_ex = sources.getInfoCNN(user_id, 5, "placeholder")
    seconds = int(time.time() - time_start)
    if validResultEx(result_ex):
        status = "passed"
    else:
        status = "failed"

    test_results.append({
        "name" : "getInfoCNN",
        "status" : status,
        "run_time" : str(seconds)
    })

    # Retrieve data from NPR.
    time_start = time.time()
    result_ex = sources.getInfoNPR(user_id, 5, "placeholder")
    seconds = int(time.time() - time_start)
    if validResultEx(result_ex):
        status = "passed"
    else:
        status = "failed"

    test_results.append({
        "name" : "getInfoNPR",
        "status" : status,
        "run_time" : str(seconds)
    })
    # Temporary code to insert CNN as source until this can be done in the UI.
    # data = {
    #     "source_type": "api",
    #     "location" : "CNN",
    #     "highlight_text" : "Trump"
    # }

    # Add an info source
    # time_start = time.time()
    # result = InfoSource.objects.add(data, user_id)

    # Temporary code to insert CNN as source until this can be done in the UI.
    # data = {
    #     "source_type": "api",
    #     "location" : "NPR",
    #     "highlight_text" : "Trump"
    # }

    # Add an info source
    # time_start = time.time()
    # result = InfoSource.objects.add(data, user_id)

    # Temporary code to insert CNN as source until this can be done in the UI.
    # data = {
    #     "source_type": "api",
    #     "location" : "Bing",
    #     "highlight_text" : "Trump"
    # }
    #
    # # Add an info source
    # time_start = time.time()
    # result = InfoSource.objects.add(data, user_id)

    return test_results

# Validates that the data structure built after retrieving
# external data such as from Bing, is valid.
def validResultEx(result_ex):
    if (len(result_ex) > 0
            and len(result_ex[0]['source']) > 0
            and len(result_ex[0]['title']) > 0
            and len(result_ex[0]['url']) > 0
            and len(result_ex[0]['description']) > 0):
            return True
    else:
        return False;
