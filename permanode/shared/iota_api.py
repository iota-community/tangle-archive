from __future__ import print_function
import sys

from iota import Transaction, TryteString
from http_request import HttpRequest
import json
from iota.json import JsonEncoder
from api_commands import *
from permanode.shared.utils import transform_with_persistence, has_network_error


class IotaApi:
    def __init__(self):
        self.headers = {
            'content-type': 'application/json',
            'X-IOTA-API-Version': '1'
        }

        self.method = 'GET'
        self.url = 'http://node.iota.bar:14265'

        self.response_map = {
            'findTransactions': 'hashes',
            'getTrytes': 'trytes',
            'getInclusionStates': 'states',
            'getBalances': 'balances'
        }

    def __prepare_response(self, command, response):
        if command in self.response_map:
            return response[self.response_map[command]]

        return response

    def __make_request(self, command):
        res = HttpRequest(
                self.method,
                self.url,
                headers=self.headers,
                data=json.dumps(command, cls=JsonEncoder),
            )

        if res.response is None:
            return None, 503

        return self.__prepare_response(command['command'], res.response), res.status_code

    def get_node_info(self):
        command = get_node_info()

        return self.__make_request(command)

    def find_transactions(
            self,
            **kwargs
    ):

        command = find_transactions(**kwargs)

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

    def get_transactions_objects(self, hashes):
        transactions = []

        trytes, trytes_status_code = self.get_trytes(hashes)

        if has_network_error(trytes_status_code):
            return None

        for tryte in trytes:
            transaction = Transaction.from_tryte_string(tryte)

            transactions.append(transaction.as_json_compatible())

        hashes = [tx['hash_'] for tx in transactions]

        inclusion_states, inclusion_states_status_code = self.get_latest_inclusions(hashes)

        if has_network_error(inclusion_states_status_code):
            return None

        return transform_with_persistence(transactions, inclusion_states)

    def find_transactions_objects(self, **kwargs):
        transaction_hashes, transaction_hashes_status_code = self.find_transactions(**kwargs)

        if has_network_error(transaction_hashes_status_code):
            return None

        return self.get_transactions_objects(transaction_hashes) if transaction_hashes else list()
