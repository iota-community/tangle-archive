def transform_with_persistence(all_txs, states):
    if not all_txs or not states or len(all_txs) != len(states):
        return all_txs

    all_txs_clone = all_txs[:]
    irrelevant_props = [
        'legacy_tag',
        'attachment_timestamp',
        'attachment_timestamp_lower_bound',
        'attachment_timestamp_upper_bound',
        'hash_'
    ]
    for index, tx in enumerate(all_txs_clone):
        tx['persistence'] = states[index]
        tx['address'] = tx['address'].address
        tx['min_weight_magnitude'] = trailing_zeros(tx['hash_'])
        tx['hash'] = tx['hash_']

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


def trailing_zeros(trytes):
    trytes = TryteString(trytes)
    trits = trytes.as_trits()
    n = len(trits) - 1
    z = 0
    for i in range(0, n):
        if trits[n - i] == 0:
            z += 1
        else:
            break
    return z


def has_network_error(status_code):
    return status_code == 503 or status_code == 400


def has_no_network_error(status_code):
    return status_code == 200

def is_tag(value):
    return len(value) <= 27

def is_address(value):
    return len(value) == 90

def is_transaction(value):
    return len(value) == 81 and value.endswith('999')

def is_bundle_or_address(value):
    return len(value) == 81 and not value.endswith('999')
