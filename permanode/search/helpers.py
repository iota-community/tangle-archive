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
