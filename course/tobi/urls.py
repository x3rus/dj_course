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
                url(r'^view_activity/(?P<activity_id>[0-9]+)$', views.show_activity, name='show_activity' ),
                url(r'^view_activity/$', views.list_activitys, name='list_activitys' ),
                url(r'^login/$', 'django.contrib.auth.views.login', name="login"),
                url(r'^logout/$', 'django.contrib.auth.views.logout', name="logout"),
                # Json URL
                url(r'^json_upload_gpsfile/$', views.json_upload_gpsfile, name='json_upload_gpsfile' ),
                url(r'^json_del_activity/$', views.json_del_activity, name='json_del_activity' ),
                # TODO a supprimer
                #url(r'^new_activity/$', views.new_activity, name='new_activity' ),
              ]
 
