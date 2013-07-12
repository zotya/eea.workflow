""" Custom interfaces
"""
from zope.interface import Interface

class IWorkflow(Interface):
    """ Marker interface for workflow
    """

class IWorkflowState(Interface):
    """ Marker interface for workflow state
    """
