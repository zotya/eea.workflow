#from Testing import ZopeTestCase as ztc

from Products.Five import fiveconfigure
from Products.Five import zcml
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup


@onsetup
def setup_site():
    """Set up additional products and ZCML required to test this product.

    The @onsetup decorator causes the execution of this body to be deferred
    until the setup of the Plone site testing layer.
    """
    fiveconfigure.debug_mode = True
    import Products.Five
    zcml.load_config('meta.zcml', Products.Five)
    try:
        import Products.FiveSite
        zcml.load_config('configure.zcml', Products.FiveSite)
    except ImportError: #pyflakes, #pylint: disable-msg = W0704
        pass

    import eea.workflow
    zcml.load_config('configure.zcml', eea.workflow)
    fiveconfigure.debug_mode = False

    # We need to tell the testing framework that these products
    # should be available. This can't happen until after we have loaded
    # the ZCML.

# The order here is important: We first call the deferred function and then
# let PloneTestCase install it during Plone site setup

setup_site()
ptc.setupPloneSite(
        #products=['eea.workflow'],
        extension_profiles=['eea.workflow:default', 'eea.versions:default'],
)

class TestCase(ptc.PloneTestCase):
    """Base class used for test cases
    """
class FunctionalTestCase(ptc.FunctionalTestCase):
    """Test case class used for functional (doc-)tests
    """
