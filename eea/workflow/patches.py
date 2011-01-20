from AccessControl import ClassSecurityInfo
from Products.CMFCore.WorkflowTool import WorkflowTool
from Products.CMFPlone.log import log
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
    wfs = self.getWorkflowsFor(ob)
    for wf in wfs:
        wf.notifyCreated(ob)
    self._reindexWorkflowVariables(ob)

    notify(InitialStateCreatedEvent(ob))

WorkflowTool.notifyCreated = notifyCreated

log("PATCH: Installed patches for Products.CMFCore in eea.workflow")
