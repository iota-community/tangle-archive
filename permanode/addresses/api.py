from flask import jsonify
from permanode.addresses import addresses
from permanode.shared.payload_validator import validate_payload
from permanode.addresses.schema import address_validation_schema


@addresses.route('/addresses/<address>', methods=['GET'])
@validate_payload(address_validation_schema)
def validate_address_usage():
    return jsonify({'is_used': True})
