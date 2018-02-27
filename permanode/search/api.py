from flask import jsonify, abort
from permanode.shared.validator import *
from permanode.search import search
from permanode.search.controller import Search


@search.route('/address/<address>', methods=['GET'])
def fetch_address_data(address):
    if not is_address_with_checksum(address) or not is_address_without_checksum(address):
        abort(400)

    payload = Search().address_data(address)

    if payload is None:
        abort(404)

    return jsonify(payload)


@search.route('/bundle/<bundle>', methods=['GET'])
def fetch_bundle_data(bundle):
    if not is_bundle_hash(bundle):
        abort(400)

    payload = Search().bundle_data(bundle)

    if payload is None:
        abort(404)

    return jsonify(payload)


@search.route('/tag/<tag>', methods=['GET'])
def fetch_tag_data(tag):
    if not is_tag(tag):
        abort(400)

    payload = Search().tag_data(tag)

    if payload is None:
        abort(404)

    return jsonify(payload)


@search.route('/<search_string>', methods=['GET'])
def fetch_transaction_data(search_string):
    if not search_string or len(search_string) > 90:
        abort(400)

    payload = Search().execute(search_string)

    if payload is None:
        abort(404)

    return jsonify(payload)


@search.route('/transaction/<hash>', methods=['GET'])
def fetch_unlabeled_data(hash):
    if not is_transaction_hash(hash):
        abort(400)

    payload = Search().transaction_data(hash)

    if payload is None:
        abort(404)

    return jsonify(payload)
