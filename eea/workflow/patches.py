""" Patches for Products.CMFCore
"""
from AccessControl import ClassSecurityInfo
from eea.workflow.events import InitialStateCreatedEvent
from zope.event import notify

security = ClassSecurityInfo()

security.declarePrivate('notifyCreated')
def notifyCreated(self, ob):
    """ Notify all applicable workflows that an object has been created
        and put in its new place.

    The patch adds a single line that uses zope.event to notify of
    the IInitialStateCreatedEvent event
    """
    self._old_notifyCreated(ob)
    notify(InitialStateCreatedEvent(ob))
