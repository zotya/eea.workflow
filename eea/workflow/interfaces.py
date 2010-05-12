from zope.interface import Interface

class IHasMandatoryWorkflowFields(Interface):
    """Marker interface for objects with fields that are required for workflow transitions"""


class IValueProvider(Interface):
    """Objects of this type provide values

    The use case is this: we want to be able to interrogate various AT fields contained
    in objects if they have value; we don't want to hardcode the logic that achieves
    this, so we make it extendible by adaptation. This package also provides a default
    implementation for a component that adapts AT fields -> IValueProvider
    """

    def has_value(kwargs):
        """Returns True if the object has a value"""

    def get_value(kwargs):
        """Returns the value of this object"""


class IRequiredFor(Interface):
    """Objects of this type provide required for state

    The use case is this: we want to be able to interrogate various AT fields contained
    in objects if they are required for a specific state;
    we don't want to hardcode the logic that achieves this, so we make it
    extendible by adaptation. This package also provides a default
    implementation for a component that adapts AT fields -> IRequiredFor
    """
    def __call__(state):
        """ Is required for state?
        """

class IObjectReadiness(Interface):
    """Returns info on how ready is an object to be moved to a certain workflow state"""

    def get_info_for(state_name):
        """Returns a mapping containing statistics on object readiness for a certain state"""

    def is_ready_for(state_name):
        """Returns a bool that tells is the object is ready to be transitioned to the named state"""
