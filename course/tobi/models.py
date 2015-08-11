from django.db import models

# Mes modules
from django.contrib.auth.models import User

import time

# Create your models here.


# Fournit le PATH ou deposer le fichier incluant le nom de l'utilise et l'annee et le mois
def upload_to_gpx(instance, filename):
        return 'gpx/%s/%s/%s' % (instance.user.user.username, time.strftime("%Y/%m"),filename)

# TODO : voir pour la mise en place d'un PATH meilleur 
#        http://stackoverflow.com/questions/6350153/getting-username-in-imagefield-upload-to-path
class gpsfile_model(models.Model):
    filename = models.FileField(upload_to=upload_to_gpx)


# TODO : a ce stade le fichier gpx sera traiter a chaque fois 
#        ceci me permettra de modifier l'application sans avoir a changer
#        le modele constament. Pour l'avenir ceci pourrait devenir un prob
#        de perf ... a garder en tete.
class activity(models.Model):
    # TODO : Voir pour les autre type disponible ... 
    # https://docs.djangoproject.com/en/1.8/ref/models/fields/
    title = models.CharField(max_length=255)
    datePerformed =  models.DateField()
    dateUploaded =  models.DateField()
    description = models.TextField()
    distance= models.FloatField()
    gpxFile = gpsfile_model # TODO voir si j'en fait une clef etrangere
    ispublic = models.BooleanField(False)
    owner = models.ForeignKey(User)
    ACTIVITY_STATE= (
                        ('FL', 'Final'),
                        ('DR', 'Draft'),
                    )
    activity_status= models.CharField(max_length=2,
                                     choices=ACTIVITY_STATE,
                                     default='DR')

    def __str__(self):
        return  '='.join([
            self.title,
            self.datePerformed,
            self.owner.username,
            self.ispublic,
        ])

