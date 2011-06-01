""" Workflow scripts module
"""
#from zope.component import getMultiAdapter
from Products.CMFPlone.utils import getToolByName

def fake_transition(statechange, **kw):
    """ Fake Transition
    """
    obj = statechange.object
    plone_utils = getToolByName(obj, 'plone_utils')
    plone_utils.addPortalMessage(
            "This object does not meet transition requirements. "
            "Please follow the guidelines in meeting these requirements")
    return True
