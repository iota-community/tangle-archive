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
        hashes_for_tags, hashes_for_tags_status_code = self.api.find_transactions(tags=[tag])

        if has_network_error(hashes_for_tags_status_code):
            return None
        elif has_no_network_error(hashes_for_tags_status_code):
            if not hashes_for_tags:
                return list()

            return hashes_for_tags


class History:
    def transactions_for_hash(self, value):
        pass

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

            old_transaction_hashes = Tag.get_transaction_hashes(tag_with_nines)
            recent_transactions_hashes = self.node.transactions_for_tag(tag_with_nines)

            return {
                'type': 'tag',
                'payload': recent_transactions_hashes + old_transaction_hashes
            }

        if is_address(value):
            self.history.transactions_for_address(value)

        if is_transaction(value):
            self.history.transactions_for_hash(value)

        if is_bundle_or_address(value):
            self.history.transactions_for_bundle_or_address(value)
