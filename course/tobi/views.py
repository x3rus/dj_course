# Mise en place des racoursis de code 
from django.views import generic
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect

# Models 
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Generation de page
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render_to_response
from django.template import RequestContext

import json

# Load local modules
from .models import gpsfile # TODO a term supprimer
from .models import activity
from .forms import GpxUploadForm # TODO a term supprimer 
from .forms import UploadActivityForm

##############
#  My Views  #
##############
def IndexView(request):
    return render(request, 'tobi/index.html')
        


@login_required
def new_activity(request):
    # Handle file upload
    if request.method == 'POST':
        form = GpxUploadForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = gpsfile(filename= request.FILES['docfile'])
            newdoc.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect('/tobi/')
    else:
        form = GpxUploadForm() # A empty, unbound form

    # Load documents for the list page
    documents = gpsfile.objects.all()

    # Render list page with the documents and the form
    return render_to_response(
           'tobi/upload_file.html',
                {'documents': documents, 'form': form},
                context_instance=RequestContext(request)
            )

@login_required
def new_perf(request):
    # Handle file upload
    if request.method == 'POST':
        form = UploadActivityForm(request.POST, request.FILES)
        if form.is_valid():
            # TODO ajouter la sauvegarde :D

            # Redirect to the document list after POST
            return HttpResponseRedirect('/tobi/')
    else:
        form = UploadActivityForm() # A empty, unbound form

    # Load activity for the user connected
    activitys = activity.objects.filter(owner=request.user)

    # Render list page with the documents and the form
    return render_to_response(
           'tobi/upload_activity.html',
                {'activitys': activitys, 'form': form},
                context_instance=RequestContext(request)
            )

@login_required
#def json_upload_gpsfile(request,state):
def json_upload_gpsfile(request):
    if request.method == 'POST':
        gpsfile = request.POST.get('the_gpxfile')

        response_data = {}
        response_data['result'] = 'Good GPXfile!'
        response_data['author'] = request.user.username
        response_data['data'] = gpsfile
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )


