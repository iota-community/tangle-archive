from __future__ import print_function
from iota import Address, Bundle, Transaction, TryteString, Tag
from permanode.models import AddressModel, TransactionModel, BundleHashModel, TagModel, TransactionHashModel
from permanode.search import search
from permanode.shared.iota_api import IotaApi
import sys

def bundle_search(search_string):

    api = IotaApi()

    # 'bundles' gives: duration, and all TRANSACTION HASHES from the bundle & reattachments
    bundles, bundles_status_code = api.find_transactions(bundles=[search_string])

    print(bundles, file=sys.stderr)

    if not bundles['hashes']:
        return {

        }

    else:
        if bundles_status_code == 503 or bundles_status_code == 400:
            abort(bundles_status_code)

        elif bundles_status_code == 200:

            # uses transaction hashes from the bundle to retrieve their trytes
            transaction_trytes, transaction_trytes_status_code = api.get_trytes(bundles['hashes'])

            # creates a bundle object from all the transaction trytes
            bundle_inst = Bundle.from_tryte_strings(transaction_trytes['trytes'])
            print(bundle_inst, file=sys.stderr)

            node_info, node_info_status_code = api.get_node_info()
            print(node_info, file=sys.stderr)
            latest_solid_subtangle_milestone = node_info['latestSolidSubtangleMilestone']
            transaction_states, transaction_states_status_code = api.get_inclusion_states(bundles['hashes'], [latest_solid_subtangle_milestone])
            print(transaction_states, file=sys.stderr)

            raw_bundle = bundle_inst.as_json_compatible()
            # print(raw_bundle, file=sys.stderr)
            tx_hashes = []
            cleaned_hashes = []
            # print(tx_hashes, file=sys.stderr)
            for tx in raw_bundle:
                tx_hash = tx['hash_']

                tx_hashes.append(tx_hash)

            print(tx_hashes, file=sys.stderr)

            return {
                'transactions': tx_hashes
            }
