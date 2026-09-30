"""
WSGI config wrapper for skilltrace_project on Render.
Proxies to config.wsgi.application.
"""
import os
from config.wsgi import application

__all__ = ['application']
