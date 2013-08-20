from Products.Five import BrowserView
from eea.workflow.browser.interfaces import IAjaxWorkflowMenuView
from plone.app.layout.globals.interfaces import IViewView
from urlparse import urlsplit
from zope.interface import implements


class WorkflowMenu(BrowserView):
    """Returns the workflow menu as an independent page.

    This allows reloading it through AJAX
    """
    
    implements(IViewView)   #needed for plone viewlet registrations

    def cancel_redirect(self):
        if self.request.response.getStatus() in (302, 303):
            # Try to not redirect if requested
            self.request.response.setStatus(200)

    def __call__(self):
        url = self.request.form.get('action_url')
        if not url:
            return self.index()

        (proto, host, path, query, anchor) = urlsplit(url)
        action = query.split("workflow_action=")[-1].split('&')[0]
        self.context.content_status_modify(action)
        self.cancel_redirect()

        return self.index()
