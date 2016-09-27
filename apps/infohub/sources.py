from .models import InfoSource, Audit
from ..login_reg.models import User
import time
import urllib2
import json

####################################################################
#                                                                  #
# This file should only contain methods used to communicate with   #
# external sources, such as Bing and CNN to retrieve articles      #
#                                                                  #
####################################################################


# Gets info from all active sources the logged in user has added.
def getInfo(user_id):
    # First get the user sources from the database. Only retrieve active sources.
    user_sources = InfoSource.objects.getActive(user_id)

    # Loop and retrieve data from each source
    stories = []
    for source in user_sources:
        if source.source_type == "api" and source.location == "Bing":
            stories.extend(getInfoBing(user_id, source.max_snippets))
            pass
        elif source.source_type == "api" and source.location == "CNN":
            stories.extend(getInfoCNN(user_id, source.max_snippets))

    # We have hit all the sources. Return the data.
    return stories

# Retrieves info from Bing News.
def getInfoBing(user_id, max_snippets):
    # Get the content from the Bing News Search API
    # See https://www.microsoft.com/cognitive-services/en-us/bing-news-search-api for details.
    url = "https://api.cognitive.microsoft.com/bing/v5.0/news/?Category=World"
    api_key = "5f3b95abf31f452f8a3c4cb27a2d39f7"
    req = urllib2.Request(url)
    req.add_header('Ocp-Apim-Subscription-Key', api_key)
    resp = urllib2.urlopen(req)
    content = json.load(resp)

    # Parse the content and normalize into InfoHub format.
    stories = []
    for story in content["value"][:max_snippets]:
        stories.append({
            "source" : "Bing News",
            "title" : story["name"],
            "url" : story["url"],
            "description" : story["description"] # TODO!! Color code user selected keywords
        })

    Audit.objects.audit(user_id, "Retrieved info from Bing")
    return stories

# Retrieves info from CNN.
def getInfoCNN(user_id, max_snippets):
    # Get the content from CNN API.
    # See https://newsapi.org/cnn-api for details.
    base_url = "https://newsapi.org/v1/articles?source=cnn&sortBy=top"
    api_key = "f2666e6b10934fb29ebb6849581ab509"
    url = base_url + "&apiKey=" + api_key
    req = urllib2.Request(url)
    resp = urllib2.urlopen(req)
    content = json.load(resp)
    print "DEBUG: From CNN"
    print content

    # Parse the content and normalize into InfoHub format.
    stories = []
    for story in content["articles"][:max_snippets]:
        stories.append({
            "source" : "CNN News", # Displaying the source is required by CNN if site is public.
            "title" : story["title"],
            "url" : story["url"],
            "description" : story["description"] # TODO!! Color code user selected keywords
        })

    Audit.objects.audit(user_id, "Retrieved info from CNN")
    return stories

def getInfoNPR(user_id, max_snippets):
    #http://api.npr.org/query?id=1126&apiKey=MDI2ODkyNTcxMDE0NzQ5MzUxMTMxN2M1ZA000&format=json
    #TODO: Implement
    pass

########## Helper functions ##########

def highlightText(text, keyword):
    #TODO: Add support for multiple keywords.
    return text.replace(keyword, "<span class='highlight_text'>" + keyword + "</span>")