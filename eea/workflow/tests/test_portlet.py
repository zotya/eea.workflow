""" Test portlets
"""
from eea.workflow.tests.base import TestCase


class TestPortlet(TestCase):
    """ TestPortlet TestCase class
    """

    def afterSetUp(self):
        """ After Setup
        """
        self.setRoles(('Manager', ))


def test_suite():
    """ Test Suite
    """
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestPortlet))
    return suite
