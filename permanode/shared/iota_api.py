from http_request import HttpRequest
import json
from iota.json import JsonEncoder


class IotaApi:
    def __init__(self):
        self.headers = {
            'content-type': 'application/json',
            'X-IOTA-API-Version': '1'
        }

        self.method = None
        self.url = 'https://www.veriti.io'
        self.command = None

    def _make_request(self):
        res = HttpRequest(
                self.method,
                self.url,
                headers=self.headers,
                data=json.dumps(self.command, cls=JsonEncoder),
            )

        if res is None:
            return None, 503

        return res.response, res.status_code

    def get_node_info(self):
        self.command = {
            'command': 'getNodeInfo'
        }

        self.method = 'GET'

        return self._make_request()

    def get_neighbors(self):
        self.command = {
            'command': 'getNeighbors'
        }

        self.method = 'GET'

        return self._make_request()

    def add_neighbors(self, uris):
        self.command = {
            'command': 'addNeighbors',
            'uris': uris
        }

        self.method = 'GET'

        return self._make_request()

    def remove_neighbors(self, uris):
        self.command = {
            'command': 'removeNeighbors',
            'uris': uris
        }

        self.method = 'GET'

        return self._make_request()

    def get_tips(self):
        self.command = {
            'command': 'getTips'
        }

        self.method = 'GET'

        return self._make_request()

    def find_transactions(self, addresses=None, bundles=None, tags=None, approvees=None):
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

        if approvees:
            self.command['approvees'] = approvees

        return self._make_request()

    def get_trytes(self, hashes):
        self.command = {
            'command': 'getTrytes',
            'hashes': hashes
        }

        self.method = 'GET'

        return self._make_request()

    def get_latest_inclusions(self, transactions):
        node_info, node_info_status_code = self.get_node_info()

        if not node_info:
            return node_info, node_info_status_code

        latest_milestone = node_info['latestSolidSubtangleMilestone']
        self.command = {
            'command': 'getInclusionStates',
            'transactions': transactions,
            'tips': [latest_milestone]
        }

        self.method = 'GET'

        return self._make_request()

    def get_balances(self, addresses, threshold):
        self.command = {
            'command': 'getBalances',
            'addresses': addresses,
            'threshold': 100
        }

        self.method = 'GET'

        return self._make_request()

    def get_transactions_to_approve(self, depth):
        self.command = {
            'command': 'getTransactionsToApprove',
            'depth': depth
        }

        self.method = 'GET'

        return self._make_request()

    def attach_to_tangle(self, trunkTransaction, branchTransaction, minWeightMagnitude, trytes):
        self.command = {
            'command': 'attachToTangle',
            'trunkTransaction': trunkTransaction,
            'branchTransaction': branchTransaction,
            'minWeightMagnitude': minWeightMagnitude,
            'trytes': trytes
        }

        self.method = 'POST'

        return self._make_request()

    def interrupt_attaching_to_tangle(self):
        self.command = {
            'command': 'interruptAttachingToTangle',
        }

        self.method = 'POST'

        return self._make_request()

    def broadcast_transactions(self, trytes):
        self.command = {
            'command': 'broadcastTransactions',
            'trytes': trytes
        }

        self.method = 'POST'

        return self._make_request()

    def store_transactions(self, trytes):
        self.command = {
            'command': 'storeTransactions',
            'trytes': trytes
        }

        self.method = 'POST'

        return self._make_request()
