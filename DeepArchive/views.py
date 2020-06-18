"""
DeepArchive Views
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.template.defaultfilters import slugify
from django.views.generic import ListView
from taggit.models import Tag

from DeepArchive.models import Archive, ItemSet
from DeepArchive.forms import ArchiveForm, ItemSetForm


class ArchiveList(ListView):
    """
    Archive List and default page
    """
    model = Archive

    def get_context_data(self, **kwargs):
        context = super(ArchiveList, self).get_context_data(**kwargs)
        return context


class ArchiveViewer(ListView):
    """
    Display the set contents of an Archive based on dbname
    """
    model = ItemSet

    def get_queryset(self):
        dbname = self.kwargs['dbname']
        # return ItemSet.objects.filter(archive=dbname)
        return ItemSet.objects.order_by("title")

    def get_context_data(self, **kwargs):
        context = super(ArchiveViewer, self).get_context_data(**kwargs)
        return context


def archivecreator(request):
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
        return render(request, "DeepArchive/dbnew.html", context)


def itemsetcreator(request):
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
