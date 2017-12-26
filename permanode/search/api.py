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

        if tags_status_code == 503 or tags_status_code == 400:
            abort(tags_status_code)
        elif tags_status_code == 200:
            if not tags['hashes']:
                return jsonify({
                    'type': 'tag',
                    'payload': []
                })

            transaction_trytes, transaction_trytes_status_code = api.get_trytes(tags['hashes'])
            all_transaction_objects = []

            for tryte in transaction_trytes['trytes']:
                transaction_inst = Transaction.from_tryte_string(tryte)

                all_transaction_objects.append(transaction_inst.as_json_compatible())

            return jsonify({
                'type': 'tag',
                'payload': all_transaction_objects
            })

        return jsonify({
            'type': 'tag',
            'payload': []
        })

    if len(search_string) == 90:
        addresses, addresses_status_code = api.find_transactions(addresses=[search_string[:-9]])

        if addresses_status_code == 503 or addresses_status_code == 400:
            abort(addresses_status_code)
        elif addresses_status_code == 200:
            if not addresses['hashes']:
                return jsonify({
                    'type': 'address',
                    'payload': []
                })

            transaction_trytes, transaction_trytes_status_code = api.get_trytes(addresses['hashes'])
            all_transaction_objects = []

            for tryte in transaction_trytes['trytes']:
                transaction_inst = Transaction.from_tryte_string(tryte)

                all_transaction_objects.append(transaction_inst.as_json_compatible())

            return jsonify({
                'type': 'address',
                'payload': all_transaction_objects
            })

        return jsonify({
            'type': 'address',
            'payload': []
        })

    if len(search_string) == 81 and search_string.endswith('999'):
        transaction_trytes, transaction_trytes_status_code = api.get_trytes([search_string])

        if transaction_trytes_status_code == 503 or transaction_trytes_status_code == 400:
            abort(transaction_trytes_status_code)
        elif transaction_trytes_status_code == 200:
            if not transaction_trytes['trytes']:
                return jsonify({
                    'type': 'transaction',
                    'payload': []
                })

            all_transaction_objects = []
            for tryte in transaction_trytes['trytes']:
                transaction_inst = Transaction.from_tryte_string(tryte)
                all_transaction_objects.append(transaction_inst.as_json_compatible())

            return jsonify({
                'type': 'transaction',
                'payload': all_transaction_objects
            })

        return jsonify({
            'type': 'transaction',
            'payload': []
        })

    if len(search_string) == 81 and not search_string.endswith('999'):
        bundles, bundles_status_code = api.find_transactions(bundles=[search_string])

        if bundles_status_code == 503 or bundles_status_code == 400:
            abort(bundles_status_code)
        elif bundles_status_code == 200:
            if not bundles['hashes']:
                return jsonify({
                    'type': 'bundle',
                    'payload': []
                })

            transaction_trytes, transaction_trytes_status_code = api.get_trytes(bundles['hashes'])

            bundle_inst = Bundle.from_tryte_strings(transaction_trytes['trytes'])

            return jsonify({
                'type': 'bundle',
                'payload': bundle_inst.as_json_compatible()
            })

        return jsonify({
            'type': 'bundle',
            'payload': []
        })

    abort(404)
