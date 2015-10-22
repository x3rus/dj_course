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
import datetime

# extract gpx info
import gpxpy as mod_gpxpy

# Load local modules
from .models import gpsfile # TODO a term supprimer
from .models import gpsfile_model, activity
from .forms import GpxUploadForm # TODO a term supprimer
from .forms import UploadActivityForm

# motionless modules
from motionless import AddressMarker, LatLonMarker,DecoratedMap, CenterMap, VisibleMap
from .gpx_class import GPXHandler
import xml.sax


##############
#  My Views  #
##############
@login_required
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
def list_activitys(request):
#    private_user_activitys = activity.objects.filter(ispublic=False).filter(owner=request.user)
    user_activitys = activity.objects.filter(owner=request.user)
    return render(request, 'tobi/list_activitys.html', {'user_activitys': user_activitys,})


# TODO pour visualiser
# http://wiki.openstreetmap.org/wiki/Leaflet
# http://wiki.openstreetmap.org/wiki/Openlayers_Track_example
# https://github.com/mpetazzoni/leaflet-gpx
@login_required
def show_activity(request,activity_id):
        the_activity  = get_object_or_404(activity, pk=activity_id)


@login_required
def new_perf(request):
    # Handle file upload
    if request.method == 'POST':
        form = UploadActivityForm(request.POST, request.FILES)
        if form.is_valid():
            activity_id = form.cleaned_data['activity_id']
            # TODO ajouter la sauvegarde :D ou la suppression selon le bouton appuye
            if 'save' in request.POST:
                New_activity = get_object_or_404(activity, id=activity_id)
                New_activity.description = form.cleaned_data['description']
                New_activity.title = form.cleaned_data['title']
                New_activity.datePerformed = form.cleaned_data['datePerformed']
                New_activity.ispublic = form.cleaned_data['ispublic']
                New_activity.activity_status='FL'
                New_activity.save()
                return HttpResponseRedirect('/tobi/')
            elif 'cancel' in request.POST:
                wrong_activity = get_object_or_404(activity, id=activity_id)
                wrong_activity.delete()
                return HttpResponseRedirect('/tobi/new_perf')
            else :
                return HttpResponseRedirect('/tobi/merde_pas_suppose')

            # Redirect to the document list after POST
    else:
        form = UploadActivityForm() # A empty, unbound form

    # Load activity for the user connected
    # activitys = activity.objects.filter(owner=request.user)

    # Render list page with the documents and the form
    return render_to_response(
           'tobi/upload_activity.html',
                {'form': form},
                context_instance=RequestContext(request)
            )

#################
# Json function #
#################

@login_required
def json_del_activity(request):
    if request.method == 'POST':

        activity_id= request.POST.get('del_activity_id')
        response_data = {}
        activity_2_del = get_object_or_404(activity, pk=activity_id, owner=request.user )
        activity_2_del.delete()

        # TODO retourner FALSE erreur si l'id existe Pas
        response_data['result'] = 'Deleted activity successful!'
        response_data['success'] = True
        response_data['activity_2_del'] = activity_id
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        response_data['result'] = 'No ID feed in post !'
        response_data['success'] = False
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

@login_required
def json_upload_gpsfile(request):
    if request.method == 'POST':
        #gpsfile = gpsfile_model(filename= request.FILES('the_gpxfile'))
        #gpsfile = gpsfile_model(filename= request.POST.get('the_gpxfile'))

        # TODO rajouter une validation le systeme crash s'il y a pas de donne json complete
        # exemple si the_gpxfile_data est a None
        # print "TOTO2 " + str(request.POST)
        gpsfile = request.POST.get('the_gpxfile')
        gpsfile_data = request.POST.get('the_gpfile_data')
        gpsfile_data_flat = base64.b64decode(gpsfile_data)

       # TODO ajouter de la validation sur le type de fichier
        #gpsfile.save()

         # Create a temporary file to store gpx info
        fd, tempfile_name = tempfile.mkstemp()
        tmpfile = open(tempfile_name,'w')
        tmpfile.write(gpsfile_data_flat)
        tmpfile.close()

        gpx_basic_info = extract_gpx_basic_info(tempfile_name,gpsfile)
        response_data = {}
        response_data['result'] = 'Good GPXfile!'
        response_data['author'] = request.user.username
        response_data['start_time'] = str(gpx_basic_info['start_time']).rsplit('.',1)[0]
        response_data['end_time'] = str(gpx_basic_info['end_time'])
        response_data['length'] = round(gpx_basic_info['length'],2)
        response_data['moving_time'] = gpx_basic_info['moving_time']
        response_data['description'] = gpx_basic_info['description']
        response_data['title'] = gpx_basic_info['name']
        response_data['url_map'] = gpx_basic_info['url_map']

        # TODO faire une validation des donnees avant la sauvegarde

        drafted_activity = activity()
        drafted_activity.title = gpx_basic_info['name']
        drafted_activity.datePerformed = gpx_basic_info['start_time']
        drafted_activity.dateUploaded = datetime.datetime.now()
        drafted_activity.description =  gpx_basic_info['description']
        drafted_activity.distance= gpx_basic_info['length']
        drafted_activity.gpxFile = gpsfile_data_flat
        drafted_activity.owner = request.user

        drafted_activity.save()

        response_data['activity_id'] = drafted_activity.id

        # Clean up tempfile
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

####################
# Backend function #
####################

def extract_gpx_basic_info(gpx_file_name,original_file_name="none"):
    basic_info = {}
    basic_info['name'] = 'unknown'
    basic_info['description'] = 'unknown'
    basic_info['author'] = 'unknown'
    basic_info['email'] = 'unknown'

    gpx = mod_gpxpy.parse(open(gpx_file_name))

    if gpx.name:
        basic_info['name'] = gpx.name
    else :
        basic_info['name'] = original_file_name.rsplit('.', 1)[0]
    if gpx.description:
        basic_info['description'] = gpx.description
    if gpx.author_name:
        basic_info['author'] = gpx.author
    if gpx.author_email:
        basic_info['email'] = gpx.email

    basic_info['start_time'],basic_info['end_time'] = gpx.get_time_bounds()
    # Set value in kilometers
    basic_info['length'] = gpx.length_2d() / 1000

    moving_time, stopped_time, moving_distance, stopped_distance, max_speed = gpx.get_moving_data()
    basic_info['moving_time'] = moving_time

    # create URL for static image map
    static_map = DecoratedMap(size_x=640,size_y=600,pathweight=8,pathcolor='blue')
    parser = xml.sax.make_parser()
    parser.setContentHandler(GPXHandler(static_map))
    parser.feed(open(gpx_file_name).read())
    basic_info['url_map'] = static_map.generate_url()



    return basic_info



