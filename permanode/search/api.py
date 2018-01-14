from __future__ import print_function
import sys

from flask import jsonify, abort
from iota import Address, Bundle, Transaction, TransactionHash, TryteString, Tag
from permanode.models import AddressModel, TransactionModel, BundleHashModel, TagModel, TransactionHashModel
from permanode.search import search
from permanode.shared.iota_api import IotaApi
from permanode.search.helpers import transform_with_persistence, with_nines, Search


@search.route('/<search_string>', methods=['GET'])
def fetch_associated_info(search_string):
    if not search_string or len(search_string) > 90:
        abort(400)

    api = IotaApi()
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
