from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model

KEYSPACE = 'permanode'


class Transaction(Model):
    __table_name__ = 'transactions'
    __keyspace__ = KEYSPACE

    hash = columns.Text(primary_key=True, partition_key=True, required=True)
    date = columns.Date(partition_key=True, required=True)
    address = columns.Text(required=True)
    value = columns.BigInt(required=True)
    transaction_time = columns.Integer(required=True)
    signature_message_fragment = columns.Text()
    tag = columns.Text(required=True)
    tag_index = columns.BigInt(required=True)
    current_index = columns.Integer(required=True)
    last_index = columns.Integer(required=True)
    bundle = columns.Text(required=True)
    trunk_transaction_hash = columns.Text(required=True)
    branch_transaction_hash = columns.Text(required=True)
    nonce = columns.Text(required=True)
    min_weight_magnitude = columns.Integer(required=True)
    approvees = columns.Set(columns.Text, required=True)


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
