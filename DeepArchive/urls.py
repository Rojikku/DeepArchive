"""
DeepArchive URLs
"""

from django.urls import path
from DeepArchive import views


urlpatterns = [
    path("", views.ArchiveList.as_view(), name="archivelist"),
    path("db/<slug:dbname>", views.ArchiveContents.as_view(), name="archiveviewer"),
    path("new/db", views.archive_creator, name="archivecreator"),
    path("new/itemset", views.itemset_creator, name="itemsetcreator"),
    path("itemset/<slug:slug>", views.ItemSetDetails.as_view(), name="itemsetdetails")
]
