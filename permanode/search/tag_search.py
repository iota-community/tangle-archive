from iota import Address, Bundle, Transaction, TryteString, Tag
from permanode.models import AddressModel, TransactionModel, BundleHashModel, TagModel, TransactionHashModel
from permanode.search import search
from permanode.shared.iota_api import IotaApi
import sys


def tag_search(search_string):

    api = IotaApi()

    tags, tags_status_code = api.find_transactions(tags=[search_string])

    '''
        if the full node does not contain transactions
        with this tag, check Cassandra
    '''

    if not tags['hashes']:
        tag_ref = TagModel.objects.filter(tag=search_string)
        tag_obj = [res.as_json() for res in tag_ref]

        if not tag_obj:
            return {

            }

        txs = TransactionModel.objects.filter(id__in=[t['id'] for t in tag_obj])

        return {
            'transactions': [res.as_json() for res in txs]
        }

    else:
        if tags_status_code == 503 or tags_status_code == 400:
            abort(tags_status_code)

        elif tags_status_code == 200:
            transaction_hashes, transaction_hashes_status_code = api.get_trytes(tags['hashes'])
            all_transaction_hashes = []

            for tryte in transaction_hashes['trytes']:
                all_transaction_hashes.append(tryte[2430:2511])

            # return object, not jsonify
            return {
                'transactions': all_transaction_hashes
            }
