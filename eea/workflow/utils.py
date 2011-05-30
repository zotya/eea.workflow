from Products.Archetypes.Field import Field, TextField
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.UnicodeSplitter import process_unicode
from eea.workflow.interfaces import IFieldIsRequiredForState, IValueProvider
from zope.component import adapts
from zope.interface import Interface, implements


class ATFieldValueProvider(object):
    """An IValueProvider implementation for AT Fields"""

    implements(IValueProvider)
    adapts(Interface, Field)

    def __init__(self, context, field):
        self.context = context
        self.field = field

    def has_value(self, **kwargs):
        return bool(self.get_value())  #may trigger false positives

    def get_value(self, **kwargs):
        return self.field.getAccessor(self.context)()


class TextFieldValueProvider(ATFieldValueProvider):
    """An IValueProvider implementation for Text Fields"""

    adapts(Interface, TextField)

    def has_value(self, **kwargs):
        convert = getToolByName(self.context, 'portal_transforms').convert
        value = self.field.getAccessor(self.context)()
        text = convert('html_to_text', value).getData().strip()
        words = process_unicode(text)
        return len(words) > 1   #there should be at least 2 words, or 
                                #the field is considered empty


class ATFieldIsRequiredForState(object):
    """ An IFieldIsRequiredForState implementation for AT Fields """

    implements(IFieldIsRequiredForState)
    adapts(Interface, Field)

    def __init__(self, context, field):
        self.context = context
        self.field = field

    def __call__(self, state, **kwargs):
        ATTR = 'required_for_' + state
        return getattr(self.field, ATTR, False)

