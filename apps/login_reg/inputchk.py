#from flask import request, flash, session
import re
import datetime
from django.contrib import messages

#TODO: Implement validation of MAX_BIRTHDAY

def validateAllFields(request):
    validateNotBlank(request)
    validateNames(request)
    validatePasswords(request)
    validateEmail(request)
    validateBirthday(request)

def validateNotBlank(request):
    for key in request.POST:
        if len(request.POST[key]) < 1:
            messages.add_message(request, messages.ERROR, key + " is empty but is required.")

def validateNames(request):
    if not request.POST["First Name"].isalpha() or not request.POST["Last Name"].isalpha():
        messages.add_message(request, messages.ERROR, "Only alphamumeric characters are allowed for the first and last name.")

def validatePasswords(request):
    MIN_PASSWORD = 8
    if len(request.POST["Password"]) < MIN_PASSWORD:
        messages.add_message(request, messages.ERROR, "The password must be at least " + str(MIN_PASSWORD) + " characters. Yours is only " + str(len(request.POST["Password"])) + ".")

    if len(request.POST["Password"]) != len(request.POST["Confirmed Password"]):
        messages.add_message(request, messages.ERROR, "The password and confirmed password do not match.")

def validateEmail(request):
    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
    if not EMAIL_REGEX.match(request.POST["Email"]):
        messages.add_message(request, messages.ERROR, "The email is invalid.")

def validateBirthday(request):
    MIN_BIRTHDAY = '1900-01-01'
    #MAX_BIRTHDAY = datetime.now - ??
    if request.POST["Password"] < MIN_BIRTHDAY:
        messages.add_message(request, messages.ERROR, "Invalid birthday.")
