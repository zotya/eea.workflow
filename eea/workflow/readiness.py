from eea.workflow.interfaces import IValueProvider, IObjectReadiness
from zope.component import getMultiAdapter
from zope.interface import implements
import logging


class ObjectReadiness(object):
    """Provides information about the readiness for doing a certain transition 
    
    An object can have field that are required to be filled in before a workflow transition 
    is available for it. To implement this we look for a 'required_for_YYY' boolean,
    where YYY is the workflow state to which we want to transition. 
    In addition, if this attribute is missing, we try to call a method "required_for" 
    on the field, which receives the object instance and state name as parameters.
    """

    implements(IObjectReadiness)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def get_info_for(self, state_name):
        ATTR = 'required_for_' + state_name

        _done           = 0 #the percentage of fields required for publication that are filled in
        _optional       = 0 #fields that are not required for publication that are not filled in
        _required       = 0 #the fields required for publication that are filled in
        _total_required = 0 #the number of fields that are required to be filled in for the `state_name`
        _total          = 0 #the grand total of fields

        for field in self.context.schema.fields():  #we assume AT here
            _total += 1

            info = getMultiAdapter([self.context, field], interface=IValueProvider)
            has_value = info.has_value()

            if hasattr(field, ATTR):
                is_needed = getattr(field, ATTR)
            elif hasattr(field, 'required_for'):
                is_needed = field.required_for(self.context, state)
            else:
                is_needed = False

            if is_needed:
                _total_required += 1
                if has_value:
                    _required += 1
            else:
                if not has_value:
                    _optional += 1

        _total_required = _total_required or 1  #avoid division by 0
        _done = int(float(_required) / float(_total_required) * 100.0)

        return {
                'done':_done,
                'required':_required,
                'publishing':_total_required,   #TODO:rename this to "required_for_state"
                'optional':_optional,
                'total':_total,
                }

    def is_ready_for(self, state_name):
        info = self.get_info_for(state_name)
        if info['required'] == info['publishing']:
            return True
        return False
