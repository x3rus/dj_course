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
                url(r'^new_perf/$', views.new_perf, name='new_perf' ),
#                url(r'^view_activity/$', views.view_activity, name='view_activity' ),
                url(r'^new_activity/$', views.new_activity, name='new_activity' ),
                url(r'^login/$', 'django.contrib.auth.views.login', name="login"),
                url(r'^logout/$', 'django.contrib.auth.views.logout', name="logout"),
                # Json URL
                url(r'^json_upload_gpsfile/$', views.json_upload_gpsfile, name='json_upload_gpsfile' ),
              ]
 
