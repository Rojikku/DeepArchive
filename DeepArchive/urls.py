"""
DeepArchive URLs
"""

from django.urls import path
from DeepArchive import views
from DeepArchive.models import Archive

archive_list_view = views.ArchiveList.as_view(
    queryset=Archive.objects.order_by("title"),
    context_object_name="archive_list",
    template_name="DeepArchive/dblist.html"
)

archive_viewer_view = views.ArchiveViewer.as_view(
    context_object_name="set_list",
    template_name="DeepArchive/dbview.html"
)

urlpatterns = [
    path("", archive_list_view, name="archivelist"),
    path("db/<dbname>", archive_viewer_view, name="archiveviewer"),
    path("new/db", views.archivecreator, name="archivecreator"),
    path("new/itemset", views.itemsetcreator, name="itemsetcreator"),
]
