def is_string(value):
    return isinstance(value, basestring)


def is_tag(value):
    return is_string(value) and len(value) <= 27


def is_hash(value):
    return is_string(value) and len(value) == 81


def is_address_with_checksum(value):
    return is_string(value) and len(value) == 90


def is_address_without_checksum(value):
    return is_string(value) and len(value) == 81 and not value.endswith('999')


def is_transaction_hash(value):
    return is_string(value) and is_hash(value) and value.endswith('999')


def is_bundle_hash(value):
    return is_string(value) and is_hash(value) and not value.endswith('999')


def is_bundle_or_address_without_checksum(value):
    return is_bundle_hash(value) or is_address_without_checksum(value)
