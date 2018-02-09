

def find_transactions(
        addresses=None,
        bundles=None,
        tags=None,
        approvees=None
):
    command = {
        'command': 'findTransactions'
    }

    if addresses:
        command['addresses'] = addresses

    if bundles:
        command['bundles'] = bundles

    if tags:
        command['tags'] = tags

    if approvees:
        command['approvees'] = approvees

    return command


def get_trytes(hashes):
    command = {
        'command': 'getTrytes',
        'hashes': hashes
    }

    return command


def get_inclusion_states(transactions, tips):
    command = {
        'command': 'getInclusionStates',
        'transactions': transactions,
        'tips': tips
    }

    return command


def get_balances(addresses, threshold):
    command = {
        'command': 'getBalances',
        'addresses': addresses,
        'threshold': threshold
    }

    return command


def get_node_info():
    command = {
        'command': 'getNodeInfo'
    }

    return command
