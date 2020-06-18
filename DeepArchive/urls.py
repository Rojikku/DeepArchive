"""
DeepArchive URLs
"""

from django.urls import path
from DeepArchive import views


urlpatterns = [
    path("", views.archive_list, name="archivelist"),
    path("db/<dbname>", views.archive_viewer, name="archiveviewer"),
    path("new/db", views.archive_creator, name="archivecreator"),
    path("new/itemset", views.itemset_creator, name="itemsetcreator"),
]
