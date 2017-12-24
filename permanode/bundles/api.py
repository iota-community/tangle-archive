from flask import jsonify
from permanode.bundles import bundles
from permanode.models import BundleHashModel


@bundles.route('/bundles/<bundle_hash>', methods=['GET'])
def fetch_transactions_by_address(bundle_hash):
    result = BundleHashModel.objects(bundle_hash=bundle_hash)

    return jsonify([res.get_bundle_data() for res in result])
