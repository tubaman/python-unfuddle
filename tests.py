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

    def test_good_credentials(self):
        logger.debug(self.ufd.get_projects())

    def test_bad_credentials(self):
        self.assertRaises(unfuddle.Unfuddle('keyingredient.com', 'foo', 'baz'))


class TestTickets(UnfuddleTestCase):

    def test_get_tickets(self):
        project_id = self.ufd.get_projects()[0]['id']
        self.ufd.get_tickets(project_id)


class TestTicketReports(UnfuddleTestCase):
    def test_ticket_reports(self):
        project_id = self.ufd.get_projects()[0]['id']
        reports = self.ufd.get_ticket_reports(project_id)

    def test_ticket_report(self):
        project_id = self.ufd.get_projects()[0]['id']
        report_id = self.ufd.get_ticket_reports(project_id)[0]['id']
        report = self.ufd.get_ticket_report(project_id, report_id)
        logger.debug("ticket report: %r", report)

    def test_generate_ticket_report(self):
        project_id = self.ufd.get_projects()[0]['id']
        report_id = self.ufd.get_ticket_reports(project_id)[0]['id']
        report = self.ufd.generate_ticket_report(project_id, report_id)
        logger.debug("ticket report: %r", report)

    def test_dynamic_ticket_report(self):
        project_id = self.ufd.get_projects()[0]['id']
        query = {
            'title': 'open ticket report',
            'conditions': 'status-neq-closed,status-neq-resolved',
        }
        report = self.ufd.generate_dynamic_report(project_id, query)
        logger.debug("ticket report: %r", report)
