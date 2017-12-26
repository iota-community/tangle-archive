from __future__ import print_function
import sys
from flask import jsonify, abort
from iota import Address, Bundle, Transaction, TryteString, Tag
from permanode.search import search
from permanode.shared.iota_api import IotaApi


@search.route('/<search_string>', methods=['GET'])
def fetch_associated_info(search_string):
    if not search_string or len(search_string) > 90:
        abort(400)

    api = IotaApi()

    if len(search_string) <= 27:
        tags, tags_status_code = api.find_transactions(tags=[search_string])

        if tags_status_code is 503:
            abort(503)
        else:
            return jsonify({
                'type': 'tag',
                'payload': tags
            })

    if len(search_string) is 90:
        addresses, addresses_status_code = api.find_transactions(addresses=[search_string[:-9]])

        if addresses_status_code is 503:
            abort(503)

        transaction_trytes, transaction_trytes_status_code = api.get_trytes(addresses['hashes'])
        all_transaction_objects = []

        for tryte in transaction_trytes['trytes']:
            transaction_inst = Transaction.from_tryte_string(tryte)

            all_transaction_objects.append(transaction_inst.as_json_compatible())

        return jsonify({
            'type': 'address',
            'payload': all_transaction_objects
        })

    if len(search_string) is 81 and search_string.endswith('999'):
        transaction_trytes, transaction_trytes_status_code = api.get_trytes([search_string])

        if transaction_trytes_status_code is 503:
            abort(503)

        transaction_inst = Transaction.from_tryte_string(transaction_trytes['trytes'][0])

        return jsonify({
            'type': 'transaction',
            'payload': transaction_inst.as_json_compatible()
        })

    if len(search_string) is 81 and not search_string.endswith('999'):
        bundles, bundles_status_code = api.find_transactions(bundles=[search_string])

        if bundles_status_code is 503:
            abort(503)

        transaction_trytes, transaction_trytes_status_code = api.get_trytes(bundles['hashes'])
        print('Got trytes', file=sys.stderr)

        bundle_inst = Bundle.from_tryte_strings(transaction_trytes['trytes'])

        return jsonify({
            'type': 'bundle',
            'payload': bundle_inst.as_json_compatible()
        })

    abort(404)
