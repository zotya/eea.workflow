""" Init
"""
from Products.CMFCore import DirectoryView
from zope.i18nmessageid import MessageFactory

PortletReadinessMessageFactory = MessageFactory('eea.workflow')

from eea.workflow import patches  #install patches for Products.CMFCore

__all__ = [
        patches.__name__,
        DirectoryView.__name__,
]
