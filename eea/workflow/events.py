""" Events for eea.workflow
"""
from Products.Archetypes.utils import shasattr
from zope.component.interfaces import IObjectEvent
from zope.component.interfaces import ObjectEvent
from zope.interface import implements

#Order of events triggering when an object is versioned:
#initial state creation -> object copied -> object cloned -> object versioned

class IInitialStateCreatedEvent(IObjectEvent):
    """ Event triggered when an object is initially created with a default
        workflow state
    """

class InitialStateCreatedEvent(ObjectEvent):
    """ An event object for new versions being created
    """
    implements(IInitialStateCreatedEvent)

INITIAL_ITEM_CREATION = "Initial item creation"
NEW_VERSION           = "New version"
COPIED                = "Copied"


#def _fix_bug(obj):
#   history = obj.workflow_history
#   for name, wf_entries in history.items():
#       if len(wf_entries) >= 2:
#           one = wf_entries[0]
#           two = wf_entries[1]
#           if one['action'] == two['action'] and \
#              one['actor'] == two['actor'] and \
#              one['review_state'] == two['review_state'] and \
#              one['comments'] == two['comments']:
#               wf_entries = wf_entries[1:] #removes the first entry
#               history[name] = wf_entries


def handle_workflow_initial_state_created(obj, event):
    """ Handler for the IInitialStateCreatedEvent
    """
    if not shasattr(obj, 'workflow_history'):
        return

    history = obj.workflow_history   #this is a persistent mapping

    for name, wf_entries in history.items():
        wf_entries = list(wf_entries)

        #initial creation entry has no action id
        if wf_entries[-1]['action'] != None:
            return

        wf_entries[-1]['action'] = INITIAL_ITEM_CREATION
        history[name] = tuple(wf_entries)


def handle_object_copied(obj, event):
    """ Handler for object cloned event

    The object cloned event only received the resulting object,
    with no idea to the original. This event receives the original,
    but it is triggered too soon, before the workflow history is changed
    To solve this issue we cache the UID of the original objec in the
    final object.
    """

    original = event.original
    obj._v_original_uid = original.UID()
    obj._v_original = original
    # Plone 4 copied objects don't retain workflow_history
    # so we need to copy it manually from the parent
    #obj.workflow_history = original.workflow_history.copy()


def handle_object_cloned(obj, event):
    """ Handler for object cloned event
    """
    if not shasattr(obj, 'workflow_history'):
        return

    old_history = obj._v_original.workflow_history
    history = obj.workflow_history   #this is a persistent mapping

    for name in history:
        history[name] = old_history[name] + history[name]

    for name, wf_entries in history.items():
        wf_entries = list(wf_entries)

        wf_entries[-1]['action'] = COPIED
        wf_entries[-1]['comments'] = "Copied from (uid:%s)" % \
                obj._v_original_uid
        history[name] = tuple(wf_entries)


def handle_version_created(obj, event):
    """ Handler for IVersionCreatedEvent
    """

    if not shasattr(obj, 'workflow_history'):
        return

    history = obj.workflow_history   #this is a persistent mapping

    for name, wf_entries in history.items():
        wf_entries = list(wf_entries)

        #before the version event is triggered, the object appears as copied
        if wf_entries[-1]['action'] != COPIED:
            return

        wf_entries[-1]['action'] = NEW_VERSION
        wf_entries[-1]['comments'] = "New version created based on (uid:%s)" \
                % event.original.UID()
        history[name] = tuple(wf_entries)
