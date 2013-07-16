""" Browser controllers
"""
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName

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
    def progress(self):
        """ Get progress for context based on current state
        """
        wftool = getToolByName(self.context, 'portal_workflow')
        state = wftool.getInfoFor(self.context, 'review_state')
        workflows = wftool.getWorkflowsFor(self.context)
        for wf in workflows:
            state = wf.states.get(state)
            if not state:
                continue
            return getattr(state, 'progress', 0)
        return 0
