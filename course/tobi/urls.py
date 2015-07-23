# Description :
#   Define URL use by the tobi application
# 
# Auteur : Boutry Thomas <thomas.boutry@x3rus.com>
# Date de creation : 2015-07-23
# Licence : GPL v3.
###############################################################################
from django.conf.urls import url

from . import views

urlpatterns = [
                url(r'^$', views.IndexView, name='index'),
              ]
 
