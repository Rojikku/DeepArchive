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
    BASE_DIR = path.dirname(path.dirname(path.abspath(__file__)))

    try:
        build = subprocess.check_output(
            ["git", "describe", "--tags"],
            cwd=BASE_DIR).decode('utf-8').strip()
    except:
        build = DeepArchive.__version__ + "-dev-"
        build += subprocess.check_output(
            ["git", "describe", "--tags", "--always"],
            cwd=BASE_DIR).decode('utf-8').strip()
    return "v" + build
