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

    def has_value():
        """Returns True if the object has a value"""

    def get_value():
        """Returns the value of this object"""
