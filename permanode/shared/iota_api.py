from http_request import HttpRequest
import json
from iota.json import JsonEncoder
from api_commands import *


class IotaApi:
    def __init__(self):
        self.headers = {
            'content-type': 'application/json',
            'X-IOTA-API-Version': '1'
        }

        self.method = 'GET'
        self.url = 'http://iota-tangle.io:14265'

    def __make_request(self, command):
        res = HttpRequest(
                self.method,
                self.url,
                headers=self.headers,
                data=json.dumps(command, cls=JsonEncoder),
            )

        if res is None:
            return None, 503

        return res.response, res.status_code

    def get_node_info(self):
        command = get_node_info()

        return self.__make_request(command)

    def find_transactions(
            self,
            **kwargs
    ):

        command = find_transactions(kwargs)

        return self.__make_request(command)

    def get_trytes(self, hashes):
        command = get_trytes(hashes)

        return self.__make_request(command)

    def get_latest_inclusions(self, transactions):
        node_info, node_info_status_code = self.get_node_info()

        if not node_info:
            return node_info, node_info_status_code

        latest_milestone = node_info['latestSolidSubtangleMilestone']

        command = get_inclusion_states(transactions, [latest_milestone])

        return self.__make_request(command)

    def get_balances(self, addresses, threshold=100):
        command = get_balances(addresses, threshold)

        return self.__make_request(command)
