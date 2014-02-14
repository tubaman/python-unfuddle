import json
import re
import logging
from itertools import count

import requests

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARN)


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
        assert r.status_code == 200, "GET error %d: %s" % (r.status_code,
                                                           r.text)
        return r.json()

    def post(self, path, xmldata=None):
        logger.debug("xmldata: %s" % xmldata)
        headers = {
            'content-type': 'application/xml',
            'accept': 'application/json'
        }
        r = self.s.post(self.url_prefix + path, data=xmldata.encode('utf-8'),
            headers=headers)
        assert r.status_code == 201, "POST error %d: %s" % (r.status_code,
                                                           r.text)
        created_url = r.headers['location']
        return created_url

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

    def get_ticket_by_number(self, project_id, ticket_num):
        url = "projects/%s/tickets/by_number/%s"
        return self.get(url % (project_id, ticket_num))

    def ticket_html_url(self, project_id, ticket_num):
        url = "%s/a#/projects/%s/tickets/by_number/%s"
        return url % (self.base_url, project_id, ticket_num)

    def create_ticket(self, project_id, data):
        url = "projects/%s/tickets"
        xmldata = ""
        xmldata += "<ticket>"
        for key, value in data.items():
            xmldata += "<%s>%s</%s>" % (key, value, key)
        xmldata += "</ticket>"
        created_url = self.post(url % project_id, xmldata)
        url_re = "%s/projects/(.*)/tickets/(.*)" % self.base_url
        project_id, ticket_id = re.match(url_re, created_url).groups()
        ticket_id = int(ticket_id)
        return ticket_id

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

    def create_time_entry(self, project_id, ticket_id, data):
        url = "projects/%s/tickets/%s/time_entries"
        xmldata = ""
        xmldata += "<time-entry>"
        for key, value in data.items():
            xmldata += "<%s>%s</%s>" % (key, value, key)
        xmldata += "</time-entry>"
        created_url = self.post(url % (project_id, ticket_id), xmldata)
        url_re = "%s/projects/.*/tickets/.*/time_entries/(.*)" % \
            self.base_url
        entry_id, = re.match(url_re, created_url).groups()
        entry_id = int(entry_id)
        return entry_id

    def get_severities(self, project_id):
        url = "projects/%s/severities"
        return self.get(url % project_id)
