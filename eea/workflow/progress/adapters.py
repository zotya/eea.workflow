""" Progress adapters
"""
from zope.interface import implements
from eea.workflow.progress.interfaces import IWorkflowProgress
from Products.CMFCore.utils import getToolByName

class WorkflowProgress(object):
    """ Abstract adapter for workflow progress. This will be used as a fallback
    adapter if the API can't find a more specific adapter for your workflow
    """
    implements(IWorkflowProgress)

    def __init__(self, context):
        self.context = context
        self._progress = None
        self._steps = None

    @property
    def progress(self):
        """ Progress
        """
        if self._progress is not None:
            return self._progress

        self._progress = 0
        wftool = getToolByName(self.context, 'portal_workflow')
        state = wftool.getInfoFor(self.context, 'review_state')
        workflows = wftool.getWorkflowsFor(self.context)
        for wf in workflows:
            state = wf.states.get(state)
            if not state:
                continue
            self._progress = getattr(state, 'progress', 0)
        return self._progress

    @property
    def done(self):
        """ Done
        """
        return self.progress

    @property
    def steps(self):
        """ Return a list with steps and % done like:

        [('private', 0), ('pending': 50), ('visible': 50), (published, 100)]

        """
        if self._steps is not None:
            return self._steps

        def compare(a, b):
            """ Sort
            """
            a_progress = getattr(a[1], 'progress', None) or 0
            b_progress = getattr(b[1], 'progress', None) or 0
            return cmp(a_progress, b_progress)

        self._steps = []
        wftool = getToolByName(self.context, 'portal_workflow')
        for wf in wftool.getWorkflowsFor(self.context):
            self._steps = [
                (name, getattr(item, 'progress', 0))
                for name, item in sorted(wf.states.items(), cmp=compare)]
            break
        return self._steps
