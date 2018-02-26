from flask import jsonify, abort
from permanode.shared.validator import *
from permanode.search import search
from permanode.search.controller import Search


@search.route('/<search_string>', methods=['GET'])
def fetch_transactions_meta_for(search_string):
    if not search_string or len(search_string) > 90:
        abort(400)

    payload = Search().execute(search_string)

    if payload is None:
        abort(404)

    return jsonify(payload)


@search.route('/address/<address>', methods=['GET'])
def fetch_transactions_for_address(address):
    if not is_address_with_checksum(address) or not is_address_without_checksum(address):
        abort(400)

    payload = Search().transactions_for_address(address)

    if payload is None:
        abort(404)

    return jsonify(payload)


@search.route('/tag/<tag>', methods=['GET'])
def fetch_transaction_hashes_for_tag(tag):
    if not is_tag(tag):
        abort(400)

    payload = Search().transactions_hashes_for_tag(tag)

    if payload is None:
        abort(404)

    return jsonify(payload)


@search.route('/bundle/<bundle>', methods=['GET'])
def fetch_transaction_hashes_for_bundle(bundle):
    if not is_bundle_hash(bundle):
        abort(400)

    payload = Search().transactions_for_bundle_hash(bundle)

    if payload is None:
        abort(404)

    return jsonify(payload)


@search.route('/transaction/<hash>', methods=['GET'])
def fetch_transaction_meta(hash):
    if not is_transaction_hash(hash):
        abort(400)

    payload = Search().transaction_meta(hash)

    if payload is None:
        abort(404)

    return jsonify(payload)
