from __future__ import print_function
import sys

from iota import Bundle, Transaction, TryteString
from permanode.models import Address,\
    Transaction as TransactionModel, Bundle, Tag,\
    TransactionHash, TransactionObject
from permanode.shared.iota_api import IotaApi
from permanode.shared.utils import *


class Search:
    def __init__(self):
        self.api = IotaApi()

    def transactions_for_address(self, address):
        address_without_checksum = address[:-9] if len(
            address
        ) == 90 else address

        old_transactions = TransactionModel.from_address(address_without_checksum)
        recent_transactions = self.api.find_transactions_objects(addresses=[address_without_checksum])
        balance = self.api.find_balance([address_without_checksum])

        return {
            'type': 'address',
            'payload': {
                'balance': balance,
                'transactions': old_transactions + recent_transactions  # noqa: E501
            }
        }

    def transactions_hashes_for_tag(self, tag):
        tag_with_nines = with_nines(
            tag, 27 - len(tag)
        )

        old_transaction_hashes = Tag.get_transaction_hashes(tag_with_nines)
        recent_transactions_hashes, status_code = self.api.find_transactions(tags=[tag])

        if has_network_error(status_code):
            return None

        return {
            'type': 'tag',
            'payload': recent_transactions_hashes + old_transaction_hashes
        }

    def transactions_for_bundle_hash(self, bundle):
        old_transactions = TransactionModel.from_bundle_hash(bundle)
        recent_transactions = self.api.find_transactions_objects(bundles=[bundle])

        if recent_transactions is None:
            return None

        all_transactions_from_bundle = old_transactions + recent_transactions

        return all_transactions_from_bundle if all_transactions_from_bundle else None

    def transaction_object(self, hash):
        old_transaction = TransactionModel.from_transaction_hash(hash)

        if old_transaction:
            return {
                'type': 'transaction',
                'payload': old_transaction
            }

        recent_transaction = self.api.get_transactions_objects([hash])

        return {
            'type': 'transaction',
            'payload': recent_transaction
        } if recent_transaction else None

    def execute(self, value):
        if is_tag(value):
            return self.transactions_hashes_for_tag(value)

        if is_address(value):
            return self.transactions_for_address(value)

        if is_transaction(value):
            return self.transaction_object(value)

        if is_bundle_or_address(value):
            transactions_from_bundle = self.transactions_for_bundle_hash(value)

            if transactions_from_bundle:
                return {
                    'type': 'bundle',
                    'payload': transactions_from_bundle
                }

            return self.transactions_for_address(value)
