from __future__ import print_function # In python 2.7
import sys
from http_request import HttpRequest
import json


class IotaApi:
    def __init__(self):
        self.headers = {
            'content-type': 'application/json',
            'X-IOTA-API-Version': '1'
        }

        self.method = None
        self.url = 'https://iri2-api.iota.fm:443'
        self.command = None

    def _make_fullnode_request(self):
        res = HttpRequest(
                self.method,
                self.url,
                headers=self.headers,
                data=json.dumps(self.command),
            )

        return res.response, res.status_code

    def find_transactions(self, addresses=None, bundles=None, tags=None):
        self.command = {
            'command': 'findTransactions'
        }

        self.method = 'GET'

        if addresses:
            self.command['addresses'] = addresses

        if bundles:
            self.command['bundles'] = bundles

        if tags:
            self.command['tags'] = tags

        return self._make_fullnode_request()

    def get_node_info(self):
        self.command = {
            'command': 'getNodeInfo'
        }

        self.method = 'GET'

        return self._make_fullnode_request()