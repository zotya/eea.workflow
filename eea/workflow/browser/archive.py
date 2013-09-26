from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView

class Reasons(BrowserView):
    def __call__(self):
	rv = getToolByName(self.context,
	    'portal_vocabularies')['eea.workflow.reasons']
	reasons = {}
	for reason in rv.keys():
	    reasons[reason] = rv[reason].Title()
	return reasons

class ArchiveContent(BrowserView):
    def __call__(self, **kwargs):
	import pdb; pdb.set_trace()
	form = getattr(self.request, "form", {})
	self.context.archive_reason = form['workflow_reasons_radio']
	self.context.archive_initiator = form['workflow_archive_initiator']
	self.context.archive_custom_message = form.get('workflow_other_reason', '')
	self.context.setExpirationDate(DateTime())

