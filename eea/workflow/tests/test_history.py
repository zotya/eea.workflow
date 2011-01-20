from eea.versions.versions import create_version
from eea.workflow.events import COPIED
from eea.workflow.events import INITIAL_ITEM_CREATION
from eea.workflow.events import NEW_VERSION
from eea.workflow.tests.base import TestCase


class TestHistory(TestCase):

    def afterSetUp(self):
        self.setRoles(('Manager', ))

    def test_history_creation(self):
        id = self.portal.invokeFactory("Folder", 'f1')
        folder = self.portal[id]
        history = folder.workflow_history['folder_workflow']

        assert len(history) == 1
        assert history[0]['action'] == INITIAL_ITEM_CREATION

    def test_history_copy(self):
        portal = self.portal
        id     = portal.invokeFactory("Folder", 'f1')
        folder = self.portal[id]

        wftool = portal.portal_workflow
        wftool.doActionFor(folder, 'publish')

        clipb  = portal.manage_copyObjects(ids = [id])
        res    = portal.manage_pasteObjects(clipb)
        new_id = res[0]['new_id']
        foldercopy = portal[new_id]

        history = foldercopy.workflow_history['folder_workflow']

        assert len(history) == 3
        assert history[0]['action'] == INITIAL_ITEM_CREATION
        assert history[1]['action'] == 'publish'
        assert history[2]['action'] == COPIED
        assert history[2]['review_state'] == history[0]['review_state']

    def test_history_version(self):
        portal = self.portal
        id     = portal.invokeFactory("Folder", 'f1')
        folder = self.portal[id]
        wftool = portal.portal_workflow
        wftool.doActionFor(folder, 'publish')

        version = create_version(folder)
        history = version.workflow_history['folder_workflow']

        assert len(history) == 3
        assert history[0]['action'] == INITIAL_ITEM_CREATION
        assert history[1]['action'] == 'publish'
        assert history[2]['action'] == NEW_VERSION
        assert history[2]['review_state'] == history[0]['review_state']


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestHistory))
    return suite

