from Products.CMFCore import DirectoryView
from zope.i18nmessageid import MessageFactory
from eea.workflow.config import product_globals

PortletReadinessMessageFactory = MessageFactory('eea.workflow')


def initialize(context):
    """Initializer called when used as a Zope 2 product."""


from eea.workflow import patches  #install patches
patches  #pyflakes, #pylint: disable-msg = W0104
