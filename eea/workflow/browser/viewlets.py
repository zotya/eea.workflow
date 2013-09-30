""" Viewlets
"""

from plone.app.layout.viewlets.common import ViewletBase
from eea.workflow.interfaces import IObjectArchivator


class ArchiveViewlet(ViewletBase):
    """ Viewlet that appears only when the object is archived
    """

    def update(self):
        info = IObjectArchivator(self.context)
        self.info = info
