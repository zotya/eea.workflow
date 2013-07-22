""" Browser controllers
"""
from zope.component import queryAdapter
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from eea.workflow.progress.interfaces import IWorkflowProgress

class ZMIStateProgressEdit(BrowserView):
    """ ZMI edit for state progress monitoring
    """

    def setProperties(self, form):
        """ Update properties
        """
        progress = form.get('progress', 0)
        self.context.progress = progress

    def __call__(self, **kwargs):
        form = self.request.form
        form.update(kwargs)

        submit = form.get('submit', None)
        if not submit:
            return self.index()

        self.setProperties(form)

        redirect = form.get('redirect', self.__name__)
        self.request.response.redirect(
            redirect + '?manage_tabs_message=Changes saved')

class ZMIWorkflowProgressEdit(BrowserView):
    """ ZMI edit for workflow progress monitoring
    """
    def states(self):
        """ Defined states
        """
        def compare(a, b):
            """ Sort
            """
            a_progress = getattr(a[1], 'progress', None) or 0
            b_progress = getattr(b[1], 'progress', None) or 0
            return cmp(a_progress, b_progress)

        items = self.context.states.items()
        items = sorted(items, cmp=compare)
        return items

class ProgressBarView(BrowserView):
    """ Progress bar
    """
    def __init__(self, context, request):
        super(ProgressBarView, self).__init__(context, request)
        self._info = None

    @property
    def info(self):
        """ Get progress for context based on current state
        """
        if self._info is not None:
            return self._info

        wftool = getToolByName(self.context, 'portal_workflow')

        # Look for more specific adapters
        for wf in wftool.getChainFor(self.context):
            info = queryAdapter(self.context, IWorkflowProgress, name=wf)
            if not info:
                continue
            self._info = info
            return self._info

        # Fallback on generic adapter
        self._info = queryAdapter(self.context, IWorkflowProgress)
        return self._info

    @property
    def table(self):
        """ Compute visual progress bar
        """
        table = []
        current = 0
        for state, progress in self.info.steps:
            width = progress - current
            current = progress
            yield state, progress, width

class CollectionProgressBarView(ProgressBarView):
    """ Progress bar for collections
    """
