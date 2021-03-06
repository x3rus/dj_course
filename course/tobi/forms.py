# -*- coding: utf-8 -*-
from django import forms

# Model applicatif 
# TODO peut-etre a supprimer ceci est present pour test de forms les 2 from en commentaire
#from .models import activity
#from django.forms import ModelForm

# TODO : Faut mettre plus de viande mieux comprendre ce formulaire.
#        gros merci a https://github.com/axelpale/minimal-django-file-upload-example
class GpxUploadForm(forms.Form):
    docfile = forms.FileField(
            label='Select a file',
            help_text='max. 42 megabytes'
            )

    # TODO :  Voir pour merger les 2 formulaire celui d'upload qui a le fichier gpxfile
#         et le formulaire d'affichage de l'activite
class UploadActivityForm(forms.Form):
    gpxfile = forms.FileField(
            label='Select your GPX file',
            help_text='(max. 42 megabytes)',
            ) 
    title = forms.CharField(
            max_length=255,
            label = 'Activity title',
            help_text = 'Title is required'
            )

    datePerformed = forms.DateTimeField(
            label = 'When the activity was performed',
            widget = forms.DateTimeInput(attrs = {
                'readonly' : "readonly",
                }
                )
            )

    description = forms.CharField(
            label = 'Description ',
            widget = forms.Textarea(attrs = {
                'onkeyup' : "adjust_textarea(this)",
                }
                )
            )

    distance= forms.FloatField(
            label = 'Distance',
            widget = forms.NumberInput(attrs = {
                'readonly' : "readonly",
                }
                )
            )

    ispublic = forms.BooleanField(
            required=False,
            label = 'Activity is public'
            )

    activity_id = forms.CharField(
            widget=forms.HiddenInput()
            )

class ShowActivityForm(forms.Form):
    title = forms.CharField(
            max_length=255,
            label = 'Activity title',
            help_text = 'Title is required'
            )

    datePerformed = forms.DateTimeField(
            label = 'When the activity was performed',
            widget = forms.DateTimeInput(attrs = {
                'readonly' : "readonly",
                }
                )
            )

    description = forms.CharField(
            label = 'Description ',
            widget = forms.Textarea(attrs = {
                'onkeyup' : "adjust_textarea(this)",
                }
                )
            )

    distance= forms.FloatField(
            label = 'Distance',
            widget = forms.NumberInput(attrs = {
                'readonly' : "readonly",
                }
                )
            )

    ispublic = forms.BooleanField(
            required=False,
            label = 'Activity is public'
            )


