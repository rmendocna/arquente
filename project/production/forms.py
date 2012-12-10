from django import forms
import models

class PresentationInlineAdminForm(forms.ModelForm):
    class Meta:
        model = models.Presentation
        widgets = {
            'modifier':forms.HiddenInput(),
            'modified': forms.HiddenInput(),
        }