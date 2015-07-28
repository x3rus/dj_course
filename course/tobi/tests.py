from django.test import TestCase, RequestFactory



# Added modules
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import Http404, HttpResponse

# View
from .views import IndexView

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
    def test_index_view_basic(self):
        """
        Check the index page simple
        """
        response = self.client.get(reverse('tobi:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "tobi")

    def test_index_view_basic_anonymous(self):
        """
        Check the index page simple
        """
        response = self.client.get(reverse('tobi:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "login here")


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
        self.assertContains(response, "aAuthUser/ logout")



 
