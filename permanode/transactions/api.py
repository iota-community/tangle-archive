from flask import jsonify
from permanode.transactions import transactions
from permanode.models import AddressModel, TransactionModel


@transactions.route('/transactions/<address>', methods=['GET'])
def fetch_transactions_by_address(address):
    result = AddressModel.objects(address=address).limit(10)

    return jsonify([res.get_address_data() for res in result])


@transactions.route('/transactions/<transaction_hash>', methods=['GET'])
def verify_transaction_existence(transaction_hash):
    result = TransactionModel.objects(hash=transaction_hash)

    if result.count():
        return jsonify({'exists': True})

    return jsonify({'exists': False})
