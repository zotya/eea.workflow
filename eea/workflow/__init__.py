from zope.i18nmessageid import MessageFactory
PortletReadinessMessageFactory = MessageFactory('eea.workflow')


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
