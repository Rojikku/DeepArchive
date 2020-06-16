"""
Interface URLs
"""

from django.urls import path
from interface import views

urlpatterns = [
    path("", views.home, name="home"),
    path("db", views.archive, name="archive"),
    path("db/<dbname>", views.archiveviewer, name="archiveviewer"),
]
