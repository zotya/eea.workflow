from Products.Archetypes.Field import Field
from eea.workflow.interfaces import IValueProvider
from eea.workflow.interfaces import IRequiredFor
from zope.component import adapts
from zope.interface import Interface, implements


class ATFieldValueProvider(object):
    """An IValueProvider implementation for AT Fields"""

    implements(IValueProvider)
    adapts(Interface, Field)

    def __init__(self, context, field):
        self.context = context
        self.field = field

    def has_value(self):
        return bool(self.get_value())  #may trigger false positives

    def get_value(self):
        return self.field.getAccessor(self.context)()


class ATFieldRequiredFor(object):
    """ An IRequiredFor implementation for AT Fields """

    implements(IRequiredFor)
    adapts(Interface, Field)

    def __init__(self, context, field):
        self.context = context
        self.field = field

    def __call__(self, state, **kwargs):
        ATTR = 'required_for_' + state
        return getattr(field, ATTR, False)
