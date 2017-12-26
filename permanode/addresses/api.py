from flask import jsonify, abort
from cassandra.cqlengine.query import DoesNotExist, BatchQuery
from cassandra.cqlengine.query import MultipleObjectsReturned
from permanode.addresses import addresses
from permanode.shared.payload_validator import validate_payload
from permanode.addresses.schema import address_validation_schema
from permanode.models import AddressModel
from permanode.shared.iota_api import IotaApi


@addresses.route('/addresses/<address>', methods=['GET'])
def validate_address_usage(address):
    api = IotaApi()
    transactions, status_code = api.find_transactions(bundles=[
        'MDIQATJJEX9SUANUWVERJFGAFWPSQAQRRZKKYKFYKGCBEA9FH9EETUEZOPYTVK9IVCHLJXJYQXAFGRCH9'
    ])

    if not transactions:
        abort(404)

    return jsonify(transactions)


@addresses.route('/addresses/spent/<address>') # TODO: Sort out route names
def verify_address_usage(address):
    result = AddressModel.objects(address=address)

    if not result.count():
        abort(404)

    spent_from_query = result.filter(value__lt=0)

    spent = False

    try:
        spent_from_query.get()
        spent = True
    except DoesNotExist as e:
        spent = False
    except MultipleObjectsReturned as m:
        spent = True

    return jsonify({'spent': spent})


@addresses.route('/addresses/unique', methods=['GET'])
def fetch_unique_addresses():
    result = AddressModel.objects().distinct()
    return jsonify({'addresses': result.count()})
