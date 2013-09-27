""" IObjectArchived implementation
"""

from zope.annotation.factory import factory
from eea.workflow.interface import IObjectArchived
from persistent import Persistent


class ObjectArchivedAnnotationStorage(Persistent):
    """ The IObjectArchived information stored as annotation
    """
    implements (IObjectArchived)
    adapts(IBaseObject)

    is_archived    = None
    initiator      = None
    reason         = None
    custom_message = None

    def archive(self, initiator, reason, custom_message):
        self.is_archive = True
        self.initiator = initiator
        self.custom_message = custom_message

        self.__parent__.setExpirationDate(DateTime())
        #self.__parent__.reindexObject()

archive_annotation_storage = factory(ObjectArchivedAnnotationStorage)
