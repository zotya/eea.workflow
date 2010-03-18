from zope.component import adapts
from zope.interface import Interface, implements
from eea.workflow.interfaces import IValueProvider


class ObjectReadiness(object):
    """Provides information about the readiness for doing a certain transition """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def is_ready_for(self, state_name):
        attr = 'required_for_' + state_name

        _done           = 0 #the percentage of fields required for publication that are filled in
        _optional       = 0 #fields that are not required for publication that are not filled in
        _required       = 0 #the fields required for publication that are filled in
        _total_required = 0 #the number of fields that are required for publication
        _total          = 0 #the grand total of fields

        for field in self.schema.fields():
            _total += 1
            has_value = IValueProvider(field).has_value()         #

            if getattr(field, attr, False):
                _total_required += 1
                if has_value:
                    _required += 1
            else:
                if not has_value:
                    _optional += 1

        _done = int(float(_required) / float(_total_required) * 100.0)

        return {
                'done':_done,
                'required':_required,
                'publishing':_total_required,
                'optional':_optional,
                'total':_total,
                }


class ATFieldValueProvider(object):
    """An IValueProvider adapter for AT Fields"""
    implements(IValueProvider)
    adapts(Interface)

    def has_value(self):
        return bool(self.get_value())  #we assume that the return value is something not empty

    def get_value(self):
        return self.context.getAccessor(self)()
