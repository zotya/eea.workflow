""" Custom interfaces
"""
from zope.interface import Interface

class IWorkflowTool(Interface):
    """ Marker interface for portal_workflow
    """

class IWorkflow(Interface):
    """ Marker interface for workflow
    """

class IWorkflowState(Interface):
    """ Marker interface for workflow state
    """

class IBaseObject(Interface):
    """ Marker interface for Archetypes or Dexterity objects
    """
