"""
Forms for Database Models
"""
from django import forms
from DeepArchive.models import Archive, ItemSet


class ArchiveForm(forms.ModelForm):
    """Form for Archive Model"""
    class Meta:
        model = Archive
        fields = [
            'title',
            'description',
        ]

class ItemSetForm(forms.ModelForm):
    """Form for ItemSet Model"""
    class Meta:
        model = ItemSet
        fields = [
            'title',
            'archive',
            'description',
            'image',
        ]
