from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from .models import User
import bcrypt

# Default route when launching web site.
def index(request):
    # If the user is already logged in, go to the success page.
    if "userID" in request.session:
        return redirect(reverse('useradmin:success'))
    return render(request, 'login_reg/index.html')

# Used for registering a new user.
def register(request):
    if request.method == 'POST':
        result = User.objects.register(request.POST)
        # Redirect to login/registration page again if there are validation or
        # general registration errors.
        if not result["validated"] or not result["registered"]:
            for err in result["errors"]:
                messages.add_message(request, messages.ERROR, err)
            return redirect(reverse('useradmin:index'))

        # Registration succeeded. Consider the new user logged in at this point.
        request.session['userID'] = result["user"].id
        request.session['userCity'] = result["user"].city
        return redirect(reverse('info:show_profile'))
    return redirect(reverse('useradmin:index'))

# Logs in an existing user.
def login(request):
    if request.method == 'POST':
        result = User.objects.login(request.POST)
        if not result["logged_in"]:
            for err in result["errors"]:
                messages.add_message(request, messages.ERROR, err)
            return redirect(reverse('useradmin:index'))

        # User is now logged in.
        request.session['userID'] = result["user"].id
        request.session['userCity'] = result["user"].city
        # Include below if there is a need to differenciate between registration and login.
        #messages.success(request, "logged in")
        return redirect(reverse('useradmin:success'))
    return redirect(reverse('useradmin:index'))

def success(request):
    if "userID" not in request.session:
        # Prevent user from going to the success page if not logged in.
        return redirect(reverse('useradmin:index'))
    return redirect(reverse('info:index'))

def logout(request):
    if "userID" in request.session:
        del request.session["userID"]
    return redirect(reverse('useradmin:index'))
