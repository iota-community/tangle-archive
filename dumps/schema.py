from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model
from cassandra.cqlengine.usertype import UserType

KEYSPACE = 'permanode'


class Transaction(Model):
    __table_name__ = 'transactions'
    __keyspace__ = KEYSPACE

    bucket = columns.Text(primary_key=True, partition_key=True, required=True)
    hash = columns.Text(primary_key=True, required=True)
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


class TransactionObject(UserType):
    hash = columns.Text()
    bucket = columns.Text()


class Bundle(Model):
    __table_name__ = 'bundles'
    __keyspace__ = KEYSPACE

    bucket = columns.Text(primary_key=True, partition_key=True, required=True)
    bundle = columns.Text(primary_key=True, required=True)
    transactions = columns.List(columns.UserDefinedType(TransactionObject))


class Tag(Model):
    __table_name__ = 'tags'
    __keyspace__ = KEYSPACE

    bucket = columns.Text(primary_key=True, partition_key=True, required=True)
    tag = columns.Text(primary_key=True, required=True)
    transactions = columns.List(columns.UserDefinedType(TransactionObject))


class TransactionHash(Model):
    __table_name__ = 'transaction_hashes'
    __keyspace__ = KEYSPACE

    bucket = columns.Text(primary_key=True, partition_key=True, required=True)
    hash = columns.Text(primary_key=True, required=True)
    date = columns.Text(required=True)


class Address(Model):
    __table_name__ = 'addresses'
    __keyspace__ = KEYSPACE

    bucket = columns.Text(primary_key=True, partition_key=True, required=True)
    address = columns.Text(primary_key=True, required=True)
    transactions = columns.List(columns.UserDefinedType(TransactionObject))


class Approvee(Model):
    __table_name__ = 'approvees'
    __keyspace__ = KEYSPACE

    bucket = columns.Text(primary_key=True, partition_key=True, required=True)
    hash = columns.Text(primary_key=True, required=True)
    approvees = columns.List(columns.UserDefinedType(TransactionObject))
