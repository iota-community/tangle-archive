from __future__ import print_function
import sys

from flask import jsonify, abort
from permanode.shared.validator import is_valid_address
from permanode.search import search
from permanode.search.controller import Search


@search.route('/<search_string>', methods=['GET'])
def fetch_associated_info(search_string):
    if not search_string or len(search_string) > 90:
        abort(400)

    payload = Search().execute(search_string)

    if payload is None:
        abort(404)

    return jsonify(payload)


@search.route('/<address>', methods=['GET'])
def fetch_addresses(address):
    if not address or not is_valid_address(address):
        abort(400)

    payload = Search(address)

    if payload is None:
        abort(404)

    return jsonify(payload)
