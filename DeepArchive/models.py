"""
Database Models for Archive Management
"""
from django.db import models
from taggit.managers import TaggableManager

class Archive(models.Model):
    """
    Class for each Archive
    """
    title = models.CharField(max_length=50)
    description = models.TextField()
    slug = models.SlugField(unique=True, max_length=20)

    def __str__(self):
        return self.title

class ItemSet(models.Model):
    """
    Class for sets of items
    All files from a game, all songs from an album, etc.
    """
    title = models.CharField(max_length=250)
    description = models.TextField()
    added = models.DateField(auto_now_add=True)
    slug = models.SlugField(unique=True, max_length=100)
    archive = models.ManyToManyField(Archive)
    images = models.ImageField()
    tags = TaggableManager()

    def __str__(self):
        return self.title


class Item(models.Model):
    """
    An item, likely belongs to an Item Set. Songs that are part of an Album
    """
    title = models.CharField(max_length=250)
    description = models.TextField()
    added = models.DateField(auto_now_add=True)
    slug = models.SlugField(unique=True, max_length=100)
    set = models.ManyToManyField(ItemSet)
    path = models.FilePathField()

    def __str__(self):
        return self.title
