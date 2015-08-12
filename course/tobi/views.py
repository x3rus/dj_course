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

# Module for ajax response 
import json

import base64
import tempfile # use to create temporary file 
import os # for clean tempfile

# extract gpx info
import gpxpy as mod_gpxpy

# Load local modules
from .models import gpsfile # TODO a term supprimer
from .models import gpsfile_model, activity
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
def json_upload_gpsfile(request):
    if request.method == 'POST':
        #gpsfile = gpsfile_model(filename= request.FILES('the_gpxfile'))
#        gpsfile = gpsfile_model(filename= request.POST.get('the_gpxfile'))
        gpsfile = request.POST.get('the_gpxfile')
        gpsfile_data = request.POST.get('the_gpxfile_data')
        gpsfile_data_flat = base64.b64decode(gpsfile_data)

       # TODO ajouter de la validation sur le type de fichier
        #gpsfile.save()

         # Create a temporary file to store gpx info
        fd, tempfile_name = tempfile.mkstemp()
        tmpfile = open(tempfile_name,'w')
        tmpfile.write(gpsfile_data_flat)
        tmpfile.close()

        gpx_basic_info = extract_gpx_basic_info(tempfile_name)
        response_data = {}
        response_data['result'] = 'Good GPXfile!'
        response_data['author'] = request.user.username
        response_data['start_time'] = str(gpx_basic_info['start_time'])
        response_data['end_time'] = str(gpx_basic_info['end_time'])
        response_data['length'] = gpx_basic_info['length']
        response_data['moving_time'] = gpx_basic_info['moving_time']

        # TODO clean up tempfile
        os.remove(tempfile_name)

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )


def extract_gpx_basic_info(gpx_file_name):
    basic_info = {}
    basic_info['name'] = 'unknown'
    basic_info['description'] = 'unknown'
    basic_info['author'] = 'unknown'
    basic_info['email'] = 'unknown'

    gpx = mod_gpxpy.parse(open(gpx_file_name))

    if gpx.name:
        basic_info['name'] = gpx.name
        print('  GPX name: %s' % gpx.name)
    if gpx.description:
        basic_info['description'] = gpx.description
    if gpx.author:
        basic_info['author'] = gpx.author
    if gpx.email:
        basic_info['email'] = gpx.email

    basic_info['start_time'],basic_info['end_time'] = gpx.get_time_bounds()
    basic_info['length'] = gpx.length_2d()

    moving_time, stopped_time, moving_distance, stopped_distance, max_speed = gpx.get_moving_data()
    basic_info['moving_time'] = moving_time

    return basic_info



