from iota import Address, Bundle, Transaction, TransactionHash, TryteString, Tag
from permanode.models import AddressModel, TransactionModel, BundleHashModel, TagModel, TransactionHashModel
from permanode.shared.iota_api import IotaApi


def transform_with_persistence(all_txs, states):
    if not all_txs or not states or len(all_txs) != len(states):
        return all_txs

    all_txs_clone = all_txs[:]
    irrelevant_props = [
        'legacy_tag',
        'attachment_timestamp',
        'attachment_timestamp_lower_bound',
        'attachment_timestamp_upper_bound'
    ]
    for index, tx in enumerate(all_txs_clone):
        tx['persistence'] = states[index]
        tx['address'] = tx['address'].address

        for prop in irrelevant_props:
            # safe to mutate
            del tx[prop]

    return all_txs_clone


def with_nines(string, max_range):
    for i in range(max_range):
        string += str(9)

    return string


def has_all_digits(trytes):
    try:
        return trytes[0].isdigit()
    except IndexError:
        return False


class Search:
    def __init__(self, search_for):
        self.search_for = search_for
        self.api = IotaApi()

    @staticmethod
    def grab_txs_for_address_from_db(address):
        addresses_ref = AddressModel.objects.filter(address=address)
        addresses_obj = [res.as_json() for res in addresses_ref]

        if not addresses_obj:
            return list()

        return TransactionModel.objects.filter(id__in=[addr['id'] for addr in addresses_obj])

    @staticmethod
    def grab_txs_for_tag_from_db(tag):
        tag_ref = TagModel.objects.filter(tag=tag)
        tag_obj = [res.as_json() for res in tag_ref]

        if not tag_obj:
            return list()

        return TransactionModel.objects.filter(id__in=[t['id'] for t in tag_obj])

    def get_txs_for_address(self):
        address_without_checksum = self.search_for[:-9] if len(self.search_for) == 90 else self.search_for

        addresses, addresses_status_code = self.api.find_transactions(addresses=[address_without_checksum])

        all_transaction_objects = []
        if addresses_status_code == 503 or addresses_status_code == 400:
            return None
        elif addresses_status_code == 200:
            if not addresses['hashes']:
                txs = Search.grab_txs_for_address_from_db(address_without_checksum)

                for tx in txs:
                    all_transaction_objects.append(tx)

            transaction_trytes, transaction_trytes_status_code = self.api.get_trytes(addresses['hashes'])

            for tryte in transaction_trytes['trytes']:
                transaction_inst = Transaction.from_tryte_string(tryte)

                all_transaction_objects.append(transaction_inst.as_json_compatible())

            hashes = [tx['hash_'] for tx in all_transaction_objects]

            inclusion_states, inclusion_states_status_code = self.api.get_latest_inclusions(hashes)

            if inclusion_states_status_code == 503 or inclusion_states_status_code == 400:
                return None

            txs_with_persistence = transform_with_persistence(all_transaction_objects, inclusion_states['states'])

            payload = {
                'type': 'address',
                'payload': txs_with_persistence
            } if len(txs_with_persistence) > 0 else list()

            return payload

        return None

    def get_txs_for_bundle_hash(self):
        bundles, bundles_status_code = self.api.find_transactions(bundles=[self.search_for])

        if bundles_status_code == 503 or bundles_status_code == 400:
            return None
        elif bundles_status_code == 200:
            if not bundles['hashes']:
                bundle_hash_ref = BundleHashModel.objects.filter(bundle_hash=self.search_for)
                bundle_obj = [res.as_json() for res in bundle_hash_ref]

                if not bundle_obj:
                    return list()

                txs = TransactionModel.objects.filter(id__in=[t['id'] for t in bundle_obj])

                payload = {
                    'type': 'bundle',
                    'payload': [res.as_json() for res in txs]
                } if len(txs) > 0 else list()

                return payload

            transaction_trytes, transaction_trytes_status_code = self.api.get_trytes(bundles['hashes'])

            bundle_inst = Bundle.from_tryte_strings(transaction_trytes['trytes']).as_json_compatible()
            hashes = [tx['hash_'] for tx in bundle_inst]

            inclusion_states, inclusion_states_status_code = self.api.get_latest_inclusions(hashes)

            if inclusion_states_status_code == 503 or inclusion_states_status_code == 400:
                return None

            bundle_with_persistence = transform_with_persistence(bundle_inst, inclusion_states['states'])

            payload = {
                'type': 'bundle',
                'payload': bundle_with_persistence
            } if len(bundle_with_persistence) > 0 else list()

            return payload

        return None

    def get_txs_for_bundle_hash_or_address(self):
        addresses_payload = self.get_txs_for_address()

        if not isinstance(addresses_payload, dict) and addresses_payload is None:
            return None
        elif isinstance(addresses_payload, dict) and addresses_payload is not None:
            return addresses_payload

        return self.get_txs_for_bundle_hash()

    def _grab_txs_from_db(self):
        transactions_ref = TransactionHashModel.objects.filter(hash=self.search_for)
        transaction_obj = [res.as_json() for res in transactions_ref]

        if not transaction_obj:
            return list()

        txs = TransactionModel.objects.filter(id__in=[t['id'] for t in transaction_obj])

        payload = {
            'type': 'transaction',
            'payload': [res.as_json() for res in txs]
        } if len(txs) > 0 else list()

        return payload

    def _construct_transaction_objects(self, transaction_trytes):
        all_transaction_objects = []
        for tryte in transaction_trytes:
            transaction_inst = Transaction.from_tryte_string(tryte)
            all_transaction_objects.append(transaction_inst.as_json_compatible())

        hashes = [tx['hash_'] for tx in all_transaction_objects]

        inclusion_states, inclusion_states_status_code = self.api.get_latest_inclusions(hashes)

        if inclusion_states_status_code == 503 or inclusion_states_status_code == 400:
            return None

        txs_with_persistence = transform_with_persistence(all_transaction_objects, inclusion_states['states'])
        payload = {
            'type': 'transaction',
            'payload': txs_with_persistence
        } if len(txs_with_persistence) > 0 else list()

        return payload

    def get_txs(self):
        transaction_trytes, transaction_trytes_status_code = self.api.get_trytes([self.search_for])

        if transaction_trytes_status_code == 503 or transaction_trytes_status_code == 400:
            return None
        elif transaction_trytes_status_code == 200:
            if not transaction_trytes['trytes']:
                return self._grab_txs_from_db()

            return self._construct_transaction_objects(transaction_trytes['trytes'])\
                if not has_all_digits(transaction_trytes['trytes'])\
                else self._grab_txs_from_db()

        return None

    def get_txs_for_tag(self):
        full_length_tag = with_nines(self.search_for, 27 - len(self.search_for))

        tags, tags_status_code = self.api.find_transactions(tags=[full_length_tag])

        all_transaction_objects = []

        if tags_status_code == 503 or tags_status_code == 400:
            return None
        elif tags_status_code == 200:
            if not tags['hashes']:
                txs = Search.grab_txs_for_tag_from_db(full_length_tag)

                for tx in txs:
                    all_transaction_objects.append(tx)
                    
            transaction_trytes, transaction_trytes_status_code = self.api.get_trytes(tags['hashes'])

            for tryte in transaction_trytes['trytes']:
                transaction_inst = Transaction.from_tryte_string(tryte)

                all_transaction_objects.append(transaction_inst.as_json_compatible())

            hashes = [tx['hash_'] for tx in all_transaction_objects]

            inclusion_states, inclusion_states_status_code = self.api.get_latest_inclusions(hashes)

            if inclusion_states_status_code == 503 or inclusion_states_status_code == 400:
                return None

            txs_with_persistence = transform_with_persistence(all_transaction_objects, inclusion_states[
                'states'])  # Would be good to check the key

            payload = {
                'type': 'tag',
                'payload': txs_with_persistence
            } if len(txs_with_persistence) > 0 else list()

            return payload

        return None
