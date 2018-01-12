from flask import jsonify, abort
from permanode.search import search
from permanode.search.tag_search import tag_search
from permanode.search.transaction_search import transaction_search
from permanode.search.address_search import address_search
from permanode.search.bundle_search import bundle_search


@search.route('/<search_string>', methods=['GET'])
def string_search(search_string):

    nullResponse = "We could not find anything."

    '''
        verify that the search_string:
            1. is not empty,
            2. is not over 90 characters long,
            3. only contains trytes
    '''

    if not search_string or len(search_string) > 90:
        abort(400, description=nullResponse)

    if len(search_string) <= 27:
        tag_payload = tag_search(search_string)
        if tag_payload:
            return jsonify(tag_payload)
        else:
            abort(400, description=nullResponse)

    elif len(search_string) == 81 and search_string.endswith('999'):
        transaction_payload = transaction_search(search_string)
        if transaction_payload:
            return jsonify(transaction_payload)
        else:
            abort(400, description=nullResponse)

    elif len(search_string) == 90:
        address_payload = address_search(search_string)
        if address_payload:
            return jsonify(address_payload)
        else:
            abort(400, description=nullResponse)

    elif len(search_string) == 81 and not search_string.endswith('999'):
        bundle_payload = bundle_search(search_string)
        if bundle_payload:
            return jsonify(bundle_payload)
        else:
            address_payload = address_search(search_string)
            if address_payload:
                return jsonify(address_payload)
            else:
                abort(400, description=nullResponse)
