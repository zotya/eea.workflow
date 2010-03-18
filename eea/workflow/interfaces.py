from zope.interface import Interface

class IHasMandatoryWorkflowFields(Interface):
    """Marker interface for objects with fields that are required for workflow transitions"""
