"""
Database Models for Archive Management
"""
from django.db import models
from taggit.managers import TaggableManager


def image_path(instance, filename):
    """Sets image location to MEDIA_ROOT/images/Archive_Slug/Itemset_Slug"""
    return 'images/{0}/{1}/{2}'.format(instance.archive.slug, instance.slug, filename)


class Archive(models.Model):
    """
    Class for each Archive
    """
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True, max_length=20)

    def __str__(self):
        return self.title


class ItemSet(models.Model):
    """
    Class for sets of items
    All files from a game, all songs from an album, etc.
    """
    title = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    added = models.DateField(auto_now_add=True)
    slug = models.SlugField(unique=True, max_length=100)
    archive = models.ForeignKey('Archive', on_delete=models.CASCADE)
    image = models.ImageField(blank=True, upload_to=image_path)
    tags = TaggableManager(blank=True)

    def __str__(self):
        return self.title


class ItemSetImage(models.Model):
    """
    Additional images beyond the main one for an item set
    """
    iset = models.ForeignKey(ItemSet, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=image_path)

    def __str__(self):
        return self.iset.title


class Item(models.Model):
    """
    An item, likely belongs to an Item Set. Songs that are part of an Album
    """
    title = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    added = models.DateField(auto_now_add=True)
    slug = models.SlugField(unique=True, max_length=100)
    iset = models.ForeignKey('ItemSet', on_delete=models.CASCADE)
    # The below model type is useless and needs to be replaced with a different system
    filepath = models.FilePathField(path='/')

    def __str__(self):
        return self.title
