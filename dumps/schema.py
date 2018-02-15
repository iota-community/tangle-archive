from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model

KEYSPACE = 'permanode'


class Transaction(Model):
    __table_name__ = 'transactions'
    __keyspace__ = KEYSPACE

    hash = columns.Text(primary_key=True)
    address = columns.Text()
    value = columns.BigInt()
    transaction_time = columns.Integer()
    signature_message_fragment = columns.Text()
    tag = columns.Text()
    tag_index = columns.BigInt()
    current_index = columns.Integer()
    last_index = columns.Integer()
    bundle = columns.Text()
    trunk_transaction_hash = columns.Text()
    branch_transaction_hash = columns.Text()
    nonce = columns.Text()
    min_weight_magnitude = columns.Integer()
    approvees = columns.Set(columns.Text)


class Bundle(Model):
    __table_name__ = 'bundles'
    __keyspace__ = KEYSPACE

    bundle = columns.Text(primary_key=True)
    hashes = columns.Set(columns.Text)


class Tag(Model):
    __table_name__ = 'tags'
    __keyspace__ = KEYSPACE

    tag = columns.Text(primary_key=True)
    hashes = columns.Set(columns.Text)


class Address(Model):
    __table_name__ = 'addresses'
    __keyspace__ = KEYSPACE

    address = columns.Text(primary_key=True)
    hashes = columns.Set(columns.Text)


class Approvee(Model):
    __table_name__ = 'approvees'
    __keyspace__ = KEYSPACE

    hash = columns.Text(primary_key=True)
    approvees = columns.Set(columns.Text)
