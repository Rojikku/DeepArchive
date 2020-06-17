"""
Interface URLs
"""

from django.urls import path
from interface import views
from interface.models import Archive

archive_list_view = views.ArchiveList.as_view(
    queryset=Archive.objects.order_by("title"),
    context_object_name="archive_list",
    template_name="interface/dblist.html"
)

urlpatterns = [
    path("", archive_list_view, name="archivelist"),
    path("db/<dbname>", views.archiveviewer, name="archiveviewer"),
    path("newdb", views.archivecreator, name="archivecreator"),
]
