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

    # Debugging settings
    BING_ENABLED = True;
    CNN_ENABLED = True;
    NPR_ENABLED = True;

    # Loop and retrieve data from each source
    stories = {}
    for source in user_sources:
        if source.source_type == "api" and source.location == "Bing" and BING_ENABLED:
            recentStories = getInfoBing(user_id, source.max_snippets, source.highlight_text)
            if len(recentStories) > 0:
                stories["Bing"] = recentStories
        elif source.source_type == "api" and source.location == "CNN" and CNN_ENABLED:
            recentStories = getInfoCNN(user_id, source.max_snippets, source.highlight_text)
            if len(recentStories) > 0:
                stories["CNN"]  = recentStories
        elif source.source_type == "api" and source.location == "NPR" and NPR_ENABLED:
            recentStories = getInfoNPR(user_id, source.max_snippets, source.highlight_text)
            if len(recentStories) > 0:
                stories["NPR"] = recentStories

    # We have hit all the sources. Return the data.
    return stories

# Retrieves info from Bing News.
def getInfoBing(user_id, max_snippets, highlight_text):
    # Get the content from the Bing News Search API
    # See https://www.microsoft.com/cognitive-services/en-us/bing-news-search-api for details.
    url = "https://api.cognitive.microsoft.com/bing/v5.0/news/?Category=World"
    api_key = "5f3b95abf31f452f8a3c4cb27a2d39f7"
    req = urllib2.Request(url)
    req.add_header('Ocp-Apim-Subscription-Key', api_key)

    content = None
    try:
        resp = urllib2.urlopen(req)
        content = json.load(resp)
    except Exception as e:
        print "DEBUG: urlopen failed for Bing"
        Audit.objects.audit(user_id, "Failed to retrieve info from Bing")
        return []

    # Parse the content and normalize into InfoHub format.
    stories = []
    for story in content["value"][:max_snippets]:
        stories.append({
            "source" : "Bing News",
            "title" : story["name"],
            "url" : story["url"],
            "description" : story["description"],
            "highlight_text" : highlight_text,
            "image" : story["image"]["thumbnail"]["contentUrl"]
        })

    Audit.objects.audit(user_id, "Retrieved info from Bing")
    return stories

# Retrieves info from CNN.
def getInfoCNN(user_id, max_snippets, highlight_text):
    # Get the content from CNN API.
    # See https://newsapi.org/cnn-api for details.
    base_url = "https://newsapi.org/v1/articles?source=cnn&sortBy=top"
    api_key = "f2666e6b10934fb29ebb6849581ab509"
    url = base_url + "&apiKey=" + api_key
    req = urllib2.Request(url)

    content = None
    try:
        resp = urllib2.urlopen(req)
        content = json.load(resp)
    except Exception as e:
        print "DEBUG: urlopen failed for CNN"
        Audit.objects.audit(user_id, "Failed to retrieve info from CNN")
        return []

    # Parse the content and normalize into InfoHub format.
    stories = []
    previous_title = ""
    for story in content["articles"][:max_snippets + 1]: # Account for dupe stories per 9/29/2016
        # NOTE: CNN returns the first story twice (likely bug on their side),
        # so we exlicitely check for that and ignore dupes.
        if story["title"] != previous_title:
            stories.append({
                "source" : "CNN News", # Displaying the source is required by CNN if site is public.
                "title" : story["title"],
                "url" : story["url"],
                "description" : story["description"],
                "highlight_text" : highlight_text,
                "image" : story["urlToImage"]
            })
            previous_title = story["title"]

    Audit.objects.audit(user_id, "Retrieved info from CNN")
    return stories

# Retrieves info from NPR.
def getInfoNPR(user_id, max_snippets, highlight_text):
    #http://api.npr.org/query?id=1126&apiKey=MDI2ODkyNTcxMDE0NzQ5MzUxMTMxN2M1ZA000&format=json
    base_url = "http://api.npr.org/query?id=1003&format=json"
    api_key = "MDI2ODkyNTcxMDE0NzQ5MzUxMTMxN2M1ZA000"
    url = base_url + "&apiKey=" + api_key
    req = urllib2.Request(url)

    content = None
    try:
        resp = urllib2.urlopen(req)
        content = json.load(resp)
    except Exception as e:
        print "DEBUG: urlopen failed for NPR"
        Audit.objects.audit(user_id, "Failed to retrieve info from NPR")
        return []

    stories = []
    for story in content["list"]["story"][:max_snippets]:
        # NPR doesn't always send images, so use static image
        # if we can't find one in the response.
        # The static image is set in Javascript client side.
        image = ""
        if "image" in story and len(story["image"]) > 0 and "src" in story["image"][0]:
            image = story["image"][0]["src"]

        stories.append({
            "source" : "NPR",
            "title" : story["title"]["$text"],
            "url" : story["link"][0]["$text"],
            "description" : story["teaser"]["$text"],
            "highlight_text" : highlight_text,
            "image" : image
        })

    Audit.objects.audit(user_id, "Retrieved info from NPR")
    return stories
