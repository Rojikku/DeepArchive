"""
Interface Views
"""
from django.shortcuts import render

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
    return render(request, "interface/db.html")

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
