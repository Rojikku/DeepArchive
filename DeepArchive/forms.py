"""
Forms for Database Models
"""
from django import forms
from DeepArchive.models import Archive, ItemSet, ItemSetImage, Item


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
            'archive',
            'title',
            'tags',
            'image',
            'description',
        ]

class ItemSetImageForm(forms.ModelForm):
    """Form for ItemSetImages"""
    class Meta:
        model = ItemSetImage
        fields = [
            'iset',
            'image'
        ]

ItemSetImageFormSet = forms.inlineformset_factory(ItemSet, ItemSetImage, form=ItemSetImageForm, extra=1)

# class ItemForm(forms.ModelForm):
#     """Form for Items"""
#     class Meta:
#         model = Item
