# -*- coding: utf-8 -*-
from django import forms

# TODO : Faut mettre plus de viande mieux comprendre ce formulaire.
class GpxUploadForm(forms.Form):
    docfile = forms.FileField(
            label='Select a file',
            help_text='max. 42 megabytes'
            )
