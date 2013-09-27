""" IObjectArchived implementation
"""

from Products.Archetypes.interfaces import IBaseObject
from eea.workflow.interfaces import IObjectArchived, IObjectArchivator
from persistent import Persistent
from zope.annotation.factory import factory
from zope.component import adapts
from zope.interface import implements, alsoProvides
from DateTime import DateTime


class ObjectArchivedAnnotationStorage(Persistent):
    """ The IObjectArchived information stored as annotation
    """
    implements (IObjectArchivator)
    adapts(IBaseObject)

    @property
    def is_archived(self):
        """Is this object archived?"""
        return bool(IObjectArchived.providedBy(self.__parent__))

    def archive(self, context, initiator=None, reason=None, custom_message=None):
        """Archive the object"""

        now = DateTime()
        alsoProvides(context, IObjectArchived)
        context.setExpirationDate(now)

        self.archive_date   = now
        self.initiator      = initiator
        self.custom_message = custom_message
        self.reason         = reason

        self.context.reindexObject()


archive_annotation_storage = factory(ObjectArchivedAnnotationStorage, key="eea.workflow.archive")
