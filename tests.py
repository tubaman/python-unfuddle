import unittest
import netrc
import logging

import unfuddle

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARN)


class UnfuddleTestCase(unittest.TestCase):

    def get_credentials(self):
        return netrc.netrc().authenticators("unfuddle.com")

    def setUp(self):
        username, account, password = self.get_credentials()
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

    def test_get_ticket(self):
        project_id = self.ufd.get_projects()[0]['id']
        ticket_id = list(self.ufd.get_tickets(project_id))[0]['id']
        self.ufd.get_ticket(project_id, ticket_id)


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
            'conditions_string': 'status-neq-closed,status-neq-resolved',
        }
        report = self.ufd.generate_dynamic_report(project_id, query)
        logger.debug("ticket report: %r", report)


class TestTimeTracking(UnfuddleTestCase):

    def test_time_entries(self):
        projects = self.ufd.get_projects()
        seb_project, = [p for p in projects if "SEB website" in p['title']]
        project_id = seb_project['id']
        ticket_id = list(self.ufd.get_tickets(project_id))[0]['id']
        entries = self.ufd.get_time_entries(project_id, ticket_id)
        logger.debug("entries: %r", entries)

    def test_time_invested(self):
        projects = self.ufd.get_projects()
        seb_project, = [p for p in projects if "SEB website" in p['title']]
        project_id = seb_project['id']
        query = {
            'group_by': 'ticket',
            'start_date': '2014/1/1',
            'end_date': '2014/1/31',
        }
        report = self.ufd.get_time_invested(project_id, query)
        logger.debug("time invested: %r", report)
