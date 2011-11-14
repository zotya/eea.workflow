""" Workflow scripts module
"""
from Products.statusmessages.interfaces import IStatusMessage

def fake_transition(statechange, **kw):
    """ Fake Transition
    """
    obj = statechange.object
    IStatusMessage(obj.REQUEST).add(
            "This object does not meet transition requirements. "
            "Please follow the guidelines in meeting these requirements", 
            type='error')

    return True
