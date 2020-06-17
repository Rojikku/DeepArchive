"""
Give Current Version to templates
"""
from os import path
import subprocess
from django import template
import DeepArchive

register = template.Library()


@register.simple_tag
def current_version():
    """
    Generate Version and Build from GIT
    """
    return "v" + DeepArchive.__version__
