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

    def transaction_hashes_for_tag(self, tag):
        hashes_for_tags, hashes_for_tags_status_code = self.api.find_transactions(tags=[tag])

        if has_network_error(hashes_for_tags_status_code):
            return None
        elif has_no_network_error(hashes_for_tags_status_code):
            if not hashes_for_tags:
                return list()

            return hashes_for_tags

    def transactions_for_address(self, address):
        return self.api.find_transactions_objects(addresses=[address])


class Search:
    def __init__(self):
        self.node = Node()

    def transactions_for_address(self, address):
        address_without_checksum = address[:-9] if len(
            address
        ) == 90 else address

        old_transactions = TransactionModel.from_address(address_without_checksum)
        recent_transactions = self.node.transactions_for_address(address_without_checksum)

        return {
            'type': 'address',
            'payload': {
                'balance': 0,
                'transactions': old_transactions + recent_transactions  # noqa: E501
            }
        }

    def transactions_hashes_for_tag(self, tag):
        if is_tag(tag):
            tag_with_nines = with_nines(
                tag, 27 - len(tag)
            )

            old_transaction_hashes = Tag.get_transaction_hashes(tag_with_nines)
            recent_transactions_hashes = self.node.transaction_hashes_for_tag(tag_with_nines)

            return {
                'type': 'tag',
                'payload': recent_transactions_hashes + old_transaction_hashes
            }

    def execute(self, value):
        if is_tag(value):
            return self.transactions_hashes_for_tag(value)

        if is_address(value):
            return self.transactions_for_address(value)

        if is_transaction(value):
            pass

        if is_bundle_or_address(value):
            pass
