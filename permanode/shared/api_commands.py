def find_transactions(**kwargs):
    command = {
        'command': 'findTransactions'
    }

    # TODO: Validate arguments

    for key, value in kwargs.iteritems():
        command[key] = value

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
