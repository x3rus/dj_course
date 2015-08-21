# -*- coding: utf-8 -*-
from django import forms

# TODO : Faut mettre plus de viande mieux comprendre ce formulaire.
#        gros merci a https://github.com/axelpale/minimal-django-file-upload-example
class GpxUploadForm(forms.Form):
    docfile = forms.FileField(
            label='Select a file',
            help_text='max. 42 megabytes'
            )

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
            label = 'When the activity was performed'
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
            label = 'Activity is public',)

