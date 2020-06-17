"""
Interface Views
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.template.defaultfilters import slugify
from django.views.generic import ListView
from taggit.models import Tag

from interface.models import Archive
from interface.forms import ArchiveForm


class ArchiveList(ListView):
    """
    Archive List and default page
    """
    model = Archive

    def get_context_data(self, **kwargs):
        context = super(ArchiveList, self).get_context_data(**kwargs)
        return context


def archiveviewer(request, dbname):
    """
    Archive page for dbnew, and dbview
    DBnew: Create an Archive
    DBview: View an Archive
    """
    return render(request, "interface/dbview.html",
                  {
                      "dbname": dbname,
                  })


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
        return render(request, "interface/dbnew.html", context)
