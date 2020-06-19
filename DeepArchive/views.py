"""
DeepArchive Views
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.template.defaultfilters import slugify
from django.views.generic import ListView
from taggit.models import Tag

from DeepArchive.models import Archive, ItemSet
from DeepArchive.forms import ArchiveForm, ItemSetForm


def archive_list(request):
    """
    Archive List and default page
    """
    archives = Archive.objects.order_by("title")
    return render(request, 'DeepArchive/dblist.html', {
        'archive_list': archives,
    })


def archive_viewer(request, dbname):
    """
    Display the set contents of an Archive based on dbname
    """
    ver_db = get_object_or_404(Archive, slug=dbname)
    iset = ItemSet.objects.filter(archive=ver_db)
    return render(request, 'DeepArchive/dbview.html', {
        'dbname': dbname,
        'set_list': iset,
    })


def archive_creator(request):
    """Create a new Archive"""
    form = ArchiveForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            newarchive = form.save(commit=False)
            newarchive.slug = slugify(newarchive.title)
            newarchive.save()
            form.save_m2m()
            return redirect("archivelist")
    else:
        context = {
            'form': form,
        }
        return render(request, "DeepArchive/new/db.html", context)


def itemset_creator(request):
    """Create a new ItemSet"""
    form = ItemSetForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            newitemset = form.save(commit=False)
            newitemset.slug = slugify(newitemset.title)
            newitemset.save()
            form.save_m2m()
            return redirect("archivelist")
    else:
        context = {
            'form': form,
        }
        return render(request, "DeepArchive/new/itemset.html", context)
