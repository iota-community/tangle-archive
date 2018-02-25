from __future__ import print_function
import sys

from iota import Bundle, Transaction, TryteString
from permanode.models import Address,\
    Transaction as TransactionModel, Bundle, Tag,\
    TransactionHash, TransactionObject
from permanode.shared.iota_api import IotaApi
from permanode.shared.utils import *
from permanode.search.constants import *

class Node:
    def __init__(self):
        self.api = IotaApi()

    def transactions_for_tag(self, tag):
        transactions = []

        tags, tags_status_code = self.api.find_transactions(tags=[tag])

        if has_network_error(tags_status_code):
            return None
        elif has_no_network_error(tags_status_code):
            if not tags:
                return list()

            transaction_trytes, \
            transaction_trytes_status_code = self.api.get_trytes(tags)

            for tryte in transaction_trytes:
                transaction = Transaction.from_tryte_string(tryte)

                transactions.append(transaction.as_json_compatible())

            hashes = [transaction['hash_'] for transaction in transactions]

            inclusion_states, \
            inclusion_states_status_code = self.api.get_latest_inclusions(hashes)

            if has_network_error(inclusion_states_status_code):
                return None

            return transform_with_persistence(transactions, inclusion_states)


class History:
    def transactions_for_hash(self, value):
        pass

    def transactions_for_tag(self, value):
        transactions = TransactionModel.from_tag(value)

        return transactions

    def transactions_for_bundle_or_address(self, value):
        pass

    def transactions_for_address(self, value):
        pass

class Search:
    def __init__(self):
        self.history = History()
        self.node = Node()

    def execute(self, value):
        if is_tag(value):
            tag_with_nines = with_nines(
                value, 27 - len(value)
            )

            old_transactions = self.history.transactions_for_tag(tag_with_nines)

            return {
                'type': 'tag',
                'payload': old_transactions
            }

        if is_address(value):
            self.history.transactions_for_address(value)

        if is_transaction(value):
            self.history.transactions_for_hash(value)

        if is_bundle_or_address(value):
            self.history.transactions_for_bundle_or_address(value)
