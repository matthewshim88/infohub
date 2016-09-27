from django.shortcuts import render,redirect
from django.core.urlresolvers import reverse
from .models import InfoSource, Audit
from ..login_reg.models import User
from django.contrib import messages
from django import template
import time
import urllib2
import json
import adminportal
import sources

register = template.Library()
@register.filter(name='split')
def split(value, arg):
    return value.split(' ')

@register.simple_tag
def highlight(text, keyword):
    return text.replace(keyword, "<span class='highlight_text'>" + keyword + "</span>")

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
