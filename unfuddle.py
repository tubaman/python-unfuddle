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
        return self.get("projects/%s/tickets" % project_id)
