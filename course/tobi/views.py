# Mise en place des racoursis de code 
from django.views import generic
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect

# Models 
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Generation de page
from django.shortcuts import render, get_object_or_404


##############
#  My Views  #
##############
def IndexView(request):
    return render(request, 'tobi/index.html')
        
