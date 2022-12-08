import requests, urllib

HEADERS = {'Content-Type':'application/json', 'accept': 'application/json', 'user-agent': 'xbox-youtube'}

class InvidiousApi():
    def __init__(self, plugin):
        self.plugin = plugin
        self.API = urllib.unquote(plugin.get_setting('api', unicode))
        self.PROXY = urllib.unquote(plugin.get_setting('proxy', unicode))
        self.region = plugin.get_setting('region', unicode)

    def get_api(self):
        return self.API

    def get_url(self, endpoint='/api/v1/stats'):
        body = {
            "url": "{}{}".format(self.API, endpoint)
        }
        return body

    def make_request(self, URL, HEADERS, PARAMS, BODY):
        response = requests.get(URL, headers=HEADERS, params=PARAMS, json=BODY)
        if response.status_code != 200:
            self.plugin.notify(self.plugin.get_string(730).format(response.status_code), title=self.plugin.get_string(731))
            return None
        return response.json()

    def fetch(self, endpoint=None, id=None, q=None, type=None, region=None, page=None, sort_by=None, quality=None, fields=None, pretty=None):
        PARAMS = {}
        if id:
            PARAMS['id'] = id
        if q:
            PARAMS['q'] = q
        if type:
            PARAMS['type'] = type
        if region:
            PARAMS['region'] = self.region
        if page:
            PARAMS['page'] = str(page)
        if sort_by:
            PARAMS['sort_by'] = sort_by
        if quality:
            PARAMS['quality'] = quality
        if fields:
            PARAMS['fields'] = fields
        if pretty:
            PARAMS['pretty'] = pretty
        if self.plugin.get_setting('use-proxy', bool):
            return self.make_request(self.PROXY, HEADERS, PARAMS, self.get_url(endpoint))
        return make_request("{}{}".format(self.API, self.endpoint), HEADERS, PARAMS)