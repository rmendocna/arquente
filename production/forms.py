from django import forms

from . import models

from mapbox_location_field.widgets import MapAdminInput

# class PresentationInlineAdminForm(forms.ModelForm):
#     class Meta:
#         model = models.Presentation
#         widgets = {
#             'modifier':forms.HiddenInput(),
#             'modified': forms.HiddenInput(),
#         }


class PlaceForm(forms.ModelForm):

    class Meta:
        model = models.Place
        widgets = {
            'place': MapAdminInput()
        }
        exclude = []


class PresentationInlineForm(forms.ModelForm):

    class Meta:
        model = models.Presentation
        exclude = ['video', 'gallery']
