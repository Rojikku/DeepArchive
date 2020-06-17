"""
Interface Views
"""
from django.shortcuts import render, get_object_or_404
from django.template.defaultfilters import slugify
from taggit.models import Tag

from interface.models import Archive
from interface.forms import ArchiveForm

# Create your views here.


def home(request):
    """
    Homepage
    """
    return render(request, "interface/home.html")

def archive(request):
    """
    Archive List
    """
    archives = Archive.objects.order_by('title')
    form = ArchiveForm(request.POST)
    if form.is_valid():
        newarchive = form.save(commit=False)
        newarchive.slug = slugify(newarchive.title)
        newarchive.save()
        form.save_m2m()
    context = {
        'archives': archives,
        'form': form,
    }
    return render(request, "interface/db.html", context)

def archiveviewer(request, dbname):
    """
    Archive page for dbnew, and dbview
    DBnew: Create an Archive
    DBview: View an Archive
    """
    if dbname is not None:
        return render(request, "interface/dbview.html",
                      {
                          "dbname": dbname,
                      })
    else:
        return render(request, "interface/dbnew.html")
