from zope.component import getUtility, getMultiAdapter
from eea.workflow.tests.base import TestCase


class TestPortlet(TestCase):

    def afterSetUp(self):
        self.setRoles(('Manager', ))


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestPortlet))
    return suite
