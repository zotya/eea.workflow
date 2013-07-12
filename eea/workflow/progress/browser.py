""" Browser controllers
"""
from Products.Five.browser import BrowserView

class ZMIStateProgressView(BrowserView):
    """ ZMI View for state progress bar
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

class ZMIWorkflowProgressView(BrowserView):
    """ ZMI View for workflow progress bar
    """

    def states(self):
        """ Defined states
        """
        return self.context.states.items()
