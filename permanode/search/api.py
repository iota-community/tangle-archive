from flask import jsonify, abort
from permanode.search import search
from permanode.search.helpers import Search


@search.route('/<search_string>', methods=['GET'])
def fetch_associated_info(search_string):
    if not search_string or len(search_string) > 90:
        abort(400)

    search_inst = Search(search_string)

    if len(search_string) <= 27:
        payload = search_inst.get_txs_for_tag()

        if payload is None:
            abort(404)

        return jsonify(payload)

    if len(search_string) == 90:
        payload = search_inst.get_txs_for_address()

        if payload is None:
            abort(404)

        return jsonify(payload)

    if len(search_string) == 81 and search_string.endswith('999'):
        payload = search_inst.get_txs()

        if payload is None:
            abort(404)

        return jsonify(payload)

    if len(search_string) == 81 and not search_string.endswith('999'):
        payload = search_inst.get_txs_for_bundle_hash_or_address()

        if payload is None:
            abort(404)

        return jsonify(payload)

    abort(404)
