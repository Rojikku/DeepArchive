"""
DeepArchive Views
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.template.defaultfilters import slugify
from django.views.generic import ListView, DetailView
from taggit.models import Tag

from DeepArchive.models import Archive, ItemSet
from DeepArchive.forms import ArchiveForm, ItemSetForm


class ArchiveList(ListView):
    """Archive List and default page"""
    model = Archive
    queryset = Archive.objects.order_by("title")
    template_name = 'DeepArchive/dblist.html'


class ArchiveContents(ListView):
    """Display the set contents of an Archive based on dbname"""
    model = ItemSet
    template_name = 'DeepArchive/dbview.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dbname'] = self.kwargs['dbname']
        return context

    def get_queryset(self):
        """Filter by dbname"""
        dbname = self.kwargs['dbname']
        return ItemSet.objects.filter(archive__slug=dbname).order_by("title")

class ItemSetDetails(DetailView):
    """Details view of item sets"""
    model = ItemSet
    template_name = 'DeepArchive/setview.html'

def tagged(request, slug):
    """Filter based on tag"""
    tag = get_object_or_404(Tag, slug=slug)
    # Filter itemsets by tag
    sets = ItemSet.objects.filter(tags=tag)
    context = {
        'tag': tag,
        'itemset_list': sets,
    }
    return render(request, 'DeepArchive/dbview.html', context)


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
    # Autopopulate Archive Field
    prev = request.GET.get('prev', '')
    try:
        prev_entry = Archive.objects.get(slug=prev).pk
        data = {'archive': prev_entry}
    except:
        data = {}
    form = ItemSetForm(initial=data)

    if request.method == "POST":
        form = ItemSetForm(request.POST, request.FILES)
        if form.is_valid():
            newitemset = form.save(commit=False)
            newitemset.slug = slugify(newitemset.title)
            newitemset.save()
            form.save_m2m()
            prev = request.GET.get('prev', '/')
            if prev is not '/':
                prev = '/db/' + prev
            return redirect(prev)
    else:
        context = {
            'form': form,
        }
        return render(request, "DeepArchive/new/itemset.html", context)
