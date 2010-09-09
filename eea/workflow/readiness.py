from eea.workflow.interfaces import IValueProvider, IObjectReadiness, IFieldIsRequiredForState
from zope.component import getMultiAdapter
from zope.interface import implements

OTHER_METADATA_FIELDS = (
        'locallyAllowedTypes',
        'immediatelyAddableTypes',
        'id'
        )


class ObjectReadiness(object):
    """Provides information about the readiness for doing a certain transition

    An object can have field that are required to be filled in before a workflow transition
    is available for it. To implement this we look for a 'required_for_YYY' boolean,
    where YYY is the workflow state to which we want to transition.
    In addition, if this attribute is missing, we try to call a method "required_for"
    on the field, which receives the object instance and state name as parameters.
    """

    implements(IObjectReadiness)

    def __init__(self, context):
        self.context = context

    def get_info_for(self, state_name):

        #Terminology: RFS = required for state ZZZ

        rfs_required   = 0 #the number of fields that are RFS
        rfs_with_value = 0 #the fields RFS that are filled in
        optional_empty = 0 #fields that are not RFS and are not filled in
        total_fields   = 0 #the grand total of fields
        rfs_done       = 0 #the percentage of fields RFS that are filled in
        rfs_field_names = []    #the names of fields thare are RFS
        optional_with_value = []    #optional fields that have a value

        for field in self.context.schema.fields():  #we assume AT here

            if field.isMetadata or (field.getName() in OTHER_METADATA_FIELDS):
                continue

            total_fields += 1

            info = getMultiAdapter([self.context, field], interface=IValueProvider)
            has_value = info.has_value(state=state_name)

            required_for = getMultiAdapter((self.context, field), interface=IFieldIsRequiredForState)
            is_needed = required_for(state_name)

            if is_needed:
                rfs_required += 1
                if has_value:
                    rfs_with_value += 1
                else:
                    rfs_field_names.append((field.getName(), field.widget.label))
            else:
                if not has_value:
                    optional_empty += 1
                else:
                    optional_with_value.append((field, info.get_value()))

        #rfs_required = rfs_required or 1  #avoid division by 0
        rfs_done = int(float(rfs_with_value) / float(rfs_required or 1) * 100.0)

        return {
                'rfs_done':rfs_done,
                'rfs_with_value':rfs_with_value,
                'rfs_required':rfs_required,
                'optional_empty':optional_empty,
                'total_fields':total_fields,
                'rfs_field_names':rfs_field_names,
                'optional_with_value':optional_with_value,
                'extra':[]  #extra messages that will be displayed in the portlet, in the form of tuples
                            #(cssclass, text)
                }

    def is_ready_for(self, state_name):
        info = self.get_info_for(state_name)
        if info['rfs_required'] == info['rfs_with_value']:
            return True
        return False


class ObjectReadinessView(ObjectReadiness):

    def __init__(self, context, request):
        self.context = context
        self.request = request

