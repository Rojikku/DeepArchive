"""
Forms for Database Models
"""
from django import forms
from interface.models import Archive


class ArchiveForm(forms.ModelForm):
    """Form for Archive Model"""
    class Meta:
        model = Archive
        fields = [
            'title',
            'description',
        ]
