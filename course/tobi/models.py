from django.db import models

# Mes modules
from django.contrib.auth.models import User


# Create your models here.

# TODO : voir pour la mise en place d'un PATH meilleur 
#        http://stackoverflow.com/questions/6350153/getting-username-in-imagefield-upload-to-path
class gpsfile(models.Model):
    filename = models.FileField(upload_to='documents/%Y/%m/%d')


class activity(models.Model):
    # TODO : Voir pour les autre type disponible ... 
    # https://docs.djangoproject.com/en/1.8/ref/models/fields/
    title = models.CharField(max_length=255)
    text = models.CharField(max_length=255)
    datePerformed =  models.DateField()
    description = models.TextField()
    gpxFile = models.FileField(upload_to='documents/%Y/%m/%d')
    ispublic = models.BooleanField(False)
    owner = models.ForeignKey(User)
    def __str__(self):
        return  '='.join([
            self.title,
            self.datePerformed,
            self.owner.username,
            self.ispublic,
        ])

