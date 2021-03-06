from django.test import TestCase, RequestFactory



# Added modules
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import Http404, HttpResponse
from django.test.client import Client
import simplejson
#import json
#from django.utils import simplejson
import os 
import base64

# View
from .views import IndexView, new_perf, json_upload_gpsfile

# Create your tests here.

##############
## Function ##
##############

def create_user(username,password):
    u = User.objects.create_user(username, username+"x3rus.com", password)
    u.save()
    return u


#########
# TESTS #
#########


#########
# Index #
class IndexViewTests(TestCase):

    def test_index_view_basic_anonymous(self):
        """
        Check the index page simple in anonymous mode
        """
        # Rediction to the login page , ajout de follow=true pour que le test suive
        response = self.client.get(reverse('tobi:index'),follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Username")

    def test_add_new_activity_anonymous(self):
        """
        Check the index page simple in anonymous mode
        """
        # Rediction to the login page , ajout de follow=true pour que le test suive
        response = self.client.get(reverse('tobi:new_perf'),follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Username")

    def test_add_new_activity_with_json_anonymous(self):
        """
        Check the json upload activity URL  anonymous mode
        """
        # Rediction to the login page , ajout de follow=true pour que le test suive
        response = self.client.get(reverse('tobi:json_upload_gpsfile'),follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Username")




#######################
# Test With Auth User #
class TestAuthUser(TestCase):
    """
        a bunch of test with authentication required.
    """ 
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
                username='aAuthUser', email='aAuthUser@example.com', password='top_secret')

        def test_index_view_auth_user(self):
            """
        Establish a connection with aAuthUser request to Index view
        """
        # Create an instance of a GET request.
        request = self.factory.get(reverse('tobi:index'))

        # Recall that middleware are not supported. You can simulate a
        # logged-in user by setting request.user manually.
        request.user = self.user

        # Request view x3notes/AuserAuth with authenticate user aSecondUser
        response = IndexView(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Validation")

    def test_add_new_activity(self):
        """
        Establish a connecion with aAuthUser avec try to upload a gpx file.
        """
         # Create an instance of a GET request.
        request = self.factory.get(reverse('tobi:new_perf'))

        # Recall that middleware are not supported. You can simulate a
        # logged-in user by setting request.user manually.
        request.user = self.user

        # Request view x3notes/AuserAuth with authenticate user aSecondUser
        response = new_perf(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Add a new  Activity")

    def test_json_upload_activity_without_json_data(self):
        """
        Upload an activity with the json interface without any data sent
        """
         # Create an instance of a GET request.
        request = self.factory.get(reverse('tobi:json_upload_gpsfile'))

        # Recall that middleware are not supported. You can simulate a
        # logged-in user by setting request.user manually.
        request.user = self.user

        # Request view x3notes/AuserAuth with authenticate user aSecondUser
        response = json_upload_gpsfile(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "nothing to see")

    def test_json_upload_activity(self):
        """
        Upload an activity with the json interface with a gps file 
        """
        # Use gpx file and encode it in base 64
        gpx_test_file = open('./tobi/test_medias/course_avec_chien.gpx',"r")
        gps_data_b64 = base64.b64encode(gpx_test_file.read())

        dict_json = {
                    'the_gpxfile' : "course_avec_chien.gpx",
                    'the_gpxfile_data' : "toto",
                }

        json_to_send = simplejson.dumps(dict_json)

        c = Client()
        login_sucess = c.login(username=self.user.username,password='top_secret')
        if login_sucess:
           response = c.post('/tobi/json_upload_gpsfile/', json_to_send,
                                  content_type='application/json',
                                  **{'HTTP_X_REQUESTED_WITH':'XMLHttpRequest'})
           print " ========== Ze reponse"
           print response
           print " FIN reponse ============"

        self.assertEqual(response.status_code, 200)

