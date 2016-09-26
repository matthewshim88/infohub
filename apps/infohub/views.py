from django.shortcuts import render,redirect
from django.core.urlresolvers import reverse
#from .models import InfoSource
from ..login_reg.models import User
from django.contrib import messages

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
