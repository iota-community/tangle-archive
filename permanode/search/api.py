from __future__ import print_function
import sys

from flask import jsonify, abort
from permanode.shared.validator import is_valid_address, is_valid_tag
from permanode.search import search
from permanode.search.controller import Search


@search.route('/<search_string>', methods=['GET'])
def fetch_transactions(search_string):
    if not search_string or len(search_string) > 90:
        abort(400)

    payload = Search().execute(search_string)

    if payload is None:
        abort(404)

    return jsonify(payload)


@search.route('/address/<address>', methods=['GET'])
def fetch_transactions_for_address(address):
    if not address or not is_valid_address(address):
        abort(400)

    payload = Search().execute(address)

    if payload is None:
        abort(404)

    return jsonify(payload)


@search.route('/tag/<tag>', methods=['GET'])
def fetch_transaction_hashes_for_tag(tag):
    print(tag, file=sys.stderr)
    if not tag or not is_valid_tag(tag):
        abort(400)

    payload = Search().execute(tag)

    if payload is None:
        abort(404)

    return jsonify(payload)
