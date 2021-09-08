import json
import re
import logging
from itertools import count
from xml.etree import ElementTree as ET

import requests

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARN)


def to_xml(tag, data):
    """Format data as XML"""
    root = ET.Element(tag)
    for key, value in data.items():
        el = ET.SubElement(root, key)
        el.text = unicode(value)
    return ET.tostring(root, encoding="utf-8")


class Unfuddle(object):

    BASE_PATH = "/api/v1/"

    def __init__(self, account, username, password):
        self.account = account
        self.username = username
        self.password = password
        self.base_url = "https://%s.unfuddle.com" % account
        self.url_prefix = self.base_url + self.BASE_PATH
        self.session = requests.Session()
        self.session.auth = (username, password)

    def get(self, path, query=None):
        headers = {'accept': 'application/json'}
        response = self.session.get(self.url_prefix + path, data=query, headers=headers)
        assert response.status_code == 200, "GET error %d: %s" % (response.status_code,
                                                                  response.text)
        return response.json()

    def post(self, path, xmldata=None):
        logger.debug("xmldata: %s" % xmldata)
        headers = {
            'content-type': 'application/xml',
            'accept': 'application/json'
        }
        response = self.session.post(self.url_prefix + path, data=xmldata.encode('utf-8'),
            headers=headers)
        assert response.status_code == 201, "POST error %d: %s" % (response.status_code,
                                                                   response.text)
        created_url = response.headers['location']
        return created_url

    def put(self, path, xmldata=None):
        logger.debug("xmldata: %s" % xmldata)
        headers = {
            'content-type': 'application/xml',
            'accept': 'application/json'
        }
        response = self.session.put(self.url_prefix + path, data=xmldata.encode('utf-8'),
            headers=headers)
        assert response.status_code == 200, "PUT error %d: %s" % (response.status_code,
                                                                  response.text)

    def delete(self, path):
        headers = {
            'accept': 'application/json'
        }
        response = self.session.delete(self.url_prefix + path, headers=headers)
        assert response.status_code == 200, "DELETE error %d: %s" % (response.status_code,
                                                                     response.text)

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
        xmldata = to_xml("ticket", data)
        created_url = self.post(url % project_id, xmldata)
        url_re = "%s/projects/(.*)/tickets/(.*)" % self.base_url
        project_id, ticket_id = re.match(url_re, created_url).groups()
        ticket_id = int(ticket_id)
        return ticket_id

    def update_ticket(self, project_id, ticket_id, data):
        url = "projects/%s/tickets/%s"
        xmldata = to_xml("ticket", data)
        self.put(url % (project_id, ticket_id), xmldata)

    def get_ticket_reports(self, project_id=None):
        if project_id is None:
            return self.get("ticket_reports")
        else:
            return self.get("projects/%s/ticket_reports" % project_id)

    def get_ticket_report(self, report_id, project_id=None):
        if project_id is None:
            url = "ticket_reports/%s"
            return self.get(url % report_id)
        else:
            url = "projects/%s/ticket_reports/%s"
            return self.get(url % (project_id, report_id))

    def generate_ticket_report(self, report_id, project_id=None):
        if project_id is None:
            url = "ticket_reports/%s/generate"
            return self.get(url % report_id)
        else:
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
        xmldata = to_xml("time-entry", data)
        created_url = self.post(url % (project_id, ticket_id), xmldata)
        url_re = "%s/projects/.*/tickets/.*/time_entries/(.*)" % \
            self.base_url
        entry_id, = re.match(url_re, created_url).groups()
        entry_id = int(entry_id)
        return entry_id

    def delete_time_entry(self, project_id, ticket_id, entry_id):
        url = "projects/%s/tickets/%s/time_entries/%s"
        self.delete(url % (project_id, ticket_id, entry_id))

    def get_severities(self, project_id):
        url = "projects/%s/severities"
        return self.get(url % project_id)

    def get_milestones(self, project_id=None, subset=None):
        url = "milestones"
        if project_id:
            url = ("projects/%s/" % project_id) + url
        if subset:
            url += "/%s" % subset
        return self.get(url)

    def get_milestone(self, project_id, milestone_id):
            url = "projects/%s/milestones/%s"
            return self.get(url % (project_id, milestone_id))

    def get_custom_field_values(self, project_id, field_id=None):
        url = "projects/%s/custom_field_values" % project_id
        if field_id:
            url = url + ("/%s" % field_id)
        return self.get(url)
