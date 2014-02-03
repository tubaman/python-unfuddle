from itertools import count

import requests


class Unfuddle(object):

    BASE_PATH = "/api/v1/"

    def __init__(self, account, username, password):
        self.account = account
        self.username = username
        self.password = password
        self.base_url = "https://%s.unfuddle.com" % account
        self.url_prefix = self.base_url + self.BASE_PATH
        self.s = requests.Session()
        self.s.auth = (username, password)
        self.s.headers = {'accept': 'application/json'}

    def get(self, path, query=None):
        r = self.s.get(self.url_prefix + path, data=query)
        assert r.status_code == 200
        return r.json()

    def get_projects(self):
        return self.get("projects")

    def get_tickets(self, project_id):
        for page in count(1):
            tickets = self.get("projects/%s/tickets" % project_id,
                               query={'page': str(page), 'limit': 100})
            if not tickets:
                break
            for ticket in tickets:
                yield ticket

    def get_ticket(self, project_id, ticket_id):
        url = "projects/%s/tickets/%s"
        return self.get(url % (project_id, ticket_id))

    def get_ticket_reports(self, project_id):
        return self.get("projects/%s/ticket_reports" % project_id)

    def get_ticket_report(self, project_id, report_id):
        url = "projects/%s/ticket_reports/%s"
        return self.get(url % (project_id, report_id))

    def generate_ticket_report(self, project_id, report_id):
        url = "projects/%s/ticket_reports/%s/generate"
        return self.get(url % (project_id, report_id))

    def generate_dynamic_report(self, project_id, query=None):
        url = "projects/%s/ticket_reports/dynamic"
        return self.get(url % project_id, query)

    def get_time_invested(self, project_id, query=None):
        url = "projects/%s/time_invested"
        return self.get(url % project_id, query)

    def get_time_entries(self, project_id, ticket_id):
        url = "projects/%s/tickets/%s/time_entries"
        return self.get(url % (project_id, ticket_id))

    def get_severities(self, project_id):
        url = "projects/%s/severities"
        return self.get(url % project_id)
