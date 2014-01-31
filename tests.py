import unittest
import netrc
import logging

import unfuddle

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class UnfuddleTestCase(unittest.TestCase):

    def setUp(self):
        host = "unfuddle.com"
        username, account, password = netrc.netrc().authenticators(host)
        self.ufd = unfuddle.Unfuddle(account, username, password)


class TestAuth(UnfuddleTestCase):

    def testGoodCredentials(self):
        logger.debug(self.ufd.get_projects())

    def testBadCredentials(self):
        self.assertRaises(unfuddle.Unfuddle('keyingredient.com', 'foo', 'baz'))


class TestTickets(UnfuddleTestCase):

    def testGetTickets(self):
        project_id = self.ufd.get_projects()[0]['id']
        self.ufd.get_tickets(project_id)
