from permanode.models import Transaction as TransactionModel, Tag, Approvee
from permanode.shared.iota_api import IotaApi
from permanode.shared.utils import *
from permanode.shared.validator import *


class Search:
    def __init__(self):
        self.api = IotaApi()

    def address_data(self, address):
        address_without_checksum = address[:-9] if len(
            address
        ) == 90 else address

        old_transactions = TransactionModel.from_address(address_without_checksum)
        recent_transactions = self.api.find_transactions_objects(addresses=[address_without_checksum])

        # In case there is a network error
        if recent_transactions is None:
            return None

        balance = self.api.find_balance([address_without_checksum])

        return {
            'type': 'address',
            'payload': {
                'balance': balance,
                'transactions': old_transactions + recent_transactions  # noqa: E501
            }
        }

    def tag_data(self, tag):
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

    def bundle_data(self, bundle):
        old_transactions = TransactionModel.from_bundle_hash(bundle)
        recent_transactions = self.api.find_transactions_objects(bundles=[bundle])

        if recent_transactions is None:
            return None

        all_transactions_from_bundle = old_transactions + recent_transactions

        return {
            'type': 'bundle',
            'payload': all_transactions_from_bundle
        } if all_transactions_from_bundle else None

    def transaction_data(self, hash):
        old_transaction = TransactionModel.from_transaction_hash(hash)

        if old_transaction:
            return {
                'type': 'transaction',
                'payload': {
                    'transaction': old_transaction,
                    'approvees': Approvee.get_approvees_hashes(hash)
                }
            }

        recent_transaction = self.api.get_transactions_objects([hash])

        if recent_transaction is None:
            return None

        approvees = self.api.find_approvees([hash])

        if approvees is None:
            return None

        return {
            'type': 'transaction',
            'payload': {
                'transaction': recent_transaction,
                'approvees': approvees
            }
        }

    def execute(self, value):
        if is_tag(value):
            return self.tag_data(value)
        elif is_address_with_checksum(value):
            return self.address_data(value)
        elif is_transaction_hash(value):
            return self.transaction_data(value)
        elif is_bundle_or_address_without_checksum(value):
            transactions_from_bundle = self.bundle_data(value)

            if transactions_from_bundle is not None:
                return transactions_from_bundle

            return self.address_data(value)

        return None
