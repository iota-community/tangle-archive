from __future__ import print_function
from iota import Address, Bundle, Transaction, TryteString, Tag
from permanode.models import AddressModel, TransactionModel, BundleHashModel, TagModel, TransactionHashModel
from permanode.search import search
from permanode.shared.iota_api import IotaApi
from permanode.search.transaction_search import transaction_search

import sys

def address_search(search_string):

    api = IotaApi()

    if len(search_string) == 90:
        addresses, addresses_status_code = api.find_transactions(addresses=[search_string[:-9]])

        if not addresses['hashes']:
            return {

            }

        else:
            if addresses_status_code == 503 or addresses_status_code == 400:
                abort(addresses_status_code)

            elif addresses_status_code == 200:

                return address_processor(addresses)

    elif len(search_string) == 81:
        addresses, addresses_status_code = api.find_transactions(addresses=[search_string])

        if not addresses['hashes']:
            return {

            }

        else:
            if addresses_status_code == 503 or addresses_status_code == 400:
                abort(addresses_status_code)

            elif addresses_status_code == 200:

                return address_processor(addresses)

def address_processor(addresses):
    all_transaction_objects = []
    for tx_hash in addresses['hashes']:

        all_transaction_objects.append(transaction_search(tx_hash))

#             transaction_trytes, transaction_trytes_status_code = api.get_trytes(addresses['hashes'])
#             print(transaction_trytes, file=sys.stderr)
#
#             for tryte in transaction_trytes['trytes']:
#                 print(tryte, file=sys.stderr)
#
#                 all_transaction_objects.append(transaction_search(tryte[2430:2511]))
#                 transaction_inst = Transaction.from_tryte_string(tryte)
#
#                 all_transaction_objects.append(transaction_inst.as_json_compatible())

    return {
        'transactions': all_transaction_objects
    }
