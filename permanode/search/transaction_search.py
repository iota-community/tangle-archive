from __future__ import print_function
from iota import Address, Bundle, Transaction, TryteString, Tag
from permanode.models import AddressModel, TransactionModel, BundleHashModel, TagModel, TransactionHashModel
from permanode.search import search
from permanode.shared.iota_api import IotaApi
import sys

def transaction_search(search_string):

    api = IotaApi()

    transaction_trytes, transaction_trytes_status_code = api.get_trytes([search_string])

    print(transaction_trytes, file=sys.stderr)

    if transaction_trytes_status_code == 503 or transaction_trytes_status_code == 400:
        abort(transaction_trytes_status_code)
    elif transaction_trytes_status_code == 200:
        approvee_list, approvee_list_status_code = api.find_transactions(approvees=[search_string])
        node_info, node_info_status_code = api.get_node_info()
        latest_solid_subtangle_milestone = node_info['latestSolidSubtangleMilestone']
        transaction_state, transaction_state_status_code = api.get_inclusion_states([search_string], [latest_solid_subtangle_milestone])
        confirmation = transaction_state["states"][0]

        all_9s = True
        for tryte in transaction_trytes['trytes']:
            for character in tryte:
                copy = character
                try:
                    copy = int(copy)
                except ValueError as e:
                    print(e, file=sys.stderr)

                if copy == 9 or character == 9:
                    continue
                else:
                    all_9s = False
                    break
            if not all_9s:
                transaction_inst = Transaction.from_tryte_string(tryte).as_json_compatible()
                return {
                    'transaction': transaction_inst
                }

            elif all_9s:
                return {
                    # 'type': 'transaction',
                    # 'payload': 'CassandraDB case'
                }

    # IF NOT IN FULL NODE OR CassandraDB
    return {

    }
