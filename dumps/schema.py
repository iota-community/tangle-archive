from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model

KEYSPACE = 'permanode'


class Transactions(Model):
    __table_name__ = 'transactions'
    __keyspace__ = KEYSPACE

    id=columns.Text(primary_key=True)
    address = columns.Text()
    value = columns.BigInt()
    transaction_time = columns.Integer()
    hash = columns.Text()
    signature_message_fragment = columns.Text()
    tag = columns.Text()
    tag_index = columns.BigInt()
    current_index = columns.Integer()
    last_index = columns.Integer()
    bundle_hash = columns.Text()
    trunk_transaction_hash = columns.Text()
    branch_transaction_hash = columns.Text()
    nonce = columns.Text()
    min_weight_magnitude = columns.Integer()


class TransactionHash(Model):
    __table_name__ = 'transaction_hash'
    __keyspace__ = KEYSPACE

    hash = columns.Text(primary_key=True)
    id = columns.Text(primary_key=True)


class BundleHash(Model):
    __table_name__ = 'bundle_hash'
    __keyspace__ = KEYSPACE

    bundle_hash = columns.Text(primary_key=True)
    id = columns.Text(primary_key=True)


class Tag(Model):
    __table_name__ = 'tag'
    __keyspace__ = KEYSPACE

    tag = columns.Text(primary_key=True)
    id = columns.Text(primary_key=True)


class Address(Model):
    __table_name__ = 'address'
    __keyspace__ = KEYSPACE

    address = columns.Text(primary_key=True)
    id = columns.Text(primary_key=True)


class TrunkTransactionHash(Model):
    __table_name__ = 'trunk_transaction_hash'
    __keyspace__ = KEYSPACE

    trunk = columns.Text(primary_key=True)
    id = columns.Text(primary_key=True)


class BranchTransactionHash(Model):
    __table_name__ = 'branch_transaction_hash'
    __keyspace__ = KEYSPACE

    branch = columns.Text(primary_key=True)
    id = columns.Text(primary_key=True)
