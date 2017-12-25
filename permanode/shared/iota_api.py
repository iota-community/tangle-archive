from http_request import HttpRequest
import json


class IotaApi:
    def __init__(self, method):
        self.headers = {
            'content-type': 'application/json',
            'X-IOTA-API-Version': '1'
        }

        self.method = method
        self.url = 'https://tuna.iotasalad.org:14265'
        self.command = None

    def _make_fullnode_request(self):
        try:
            return HttpRequest(
                self.method,
                self.url,
                headers=self.headers,
                data=json.dumps(self.command),
            )
        except Exception as e:
            return None

    def find_transactions(self, addresses=None, bundles=None, tags=None):
        self.command = {
            'command': 'findTransactions'
        }

        if addresses:
            self.command['addresses'] = addresses

        if bundles:
            self.command['bundles'] = bundles

        if tags:
            self.command['tags'] = tags

        return self._make_fullnode_request()
