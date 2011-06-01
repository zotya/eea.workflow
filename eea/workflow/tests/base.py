""" Base module for tests
"""
from Products.Five import fiveconfigure
from Products.Five import zcml
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup


@onsetup
def setup_site():
    """ Set up additional products and ZCML required to test this product.

    The @onsetup decorator causes the execution of this body to be deferred
    until the setup of the Plone site testing layer.
    """
    fiveconfigure.debug_mode = True
    import Products.Five
    zcml.load_config('meta.zcml', Products.Five)

    import eea.workflow
    zcml.load_config('configure.zcml', eea.workflow)
    fiveconfigure.debug_mode = False


setup_site()
ptc.setupPloneSite(
        extension_profiles=['eea.workflow:default', 'eea.versions:default'],
)

class TestCase(ptc.PloneTestCase):
    """ Base class used for test cases
    """
class FunctionalTestCase(ptc.FunctionalTestCase):
    """ Test case class used for functional (doc-)tests
    """
