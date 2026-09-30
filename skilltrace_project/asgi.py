"""
ASGI config wrapper for skilltrace_project on Render.
Proxies to config.asgi.application.
"""
import os
from config.asgi import application

__all__ = ['application']
