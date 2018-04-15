from cassandra.cqlengine import columns
from cassandra.cqlengine.usertype import UserType
from cassandra.cqlengine.query import DoesNotExist
from permanode import db

KEYSPACE = 'permanode'

class Base(db.Model):
    __abstract__ = True
    __keyspace__ = KEYSPACE


class TransactionObject(db.UserType):
    hash = columns.Text()
    bucket = columns.Text()


class Transaction(Base):
    __table_name__ = "transactions"

    bucket = columns.Text(primary_key=True, partition_key=True, required=True)
    hash = columns.Text(primary_key=True, required=True)
    address = columns.Text(required=True)
    value = columns.Text(required=True)
    transaction_time = columns.Date(required=True)
    signature_message_fragment = columns.Text()
    tag = columns.Text(required=True)
    tag_index = columns.BigInt(required=True)
    current_index = columns.BigInt(required=True)
    last_index = columns.BigInt(required=True)
    bundle = columns.Text(required=True)
    trunk_transaction_hash = columns.Text(required=True)
    branch_transaction_hash = columns.Text(required=True)
    nonce = columns.Text(required=True)
    min_weight_magnitude = columns.Integer(required=True)
    persistence=columns.Boolean(required=True)

    @classmethod
    def filter(cls, buckets=list(), hashes=list()):
        transactions = list()

        for transaction in Transaction.objects.filter(bucket__in=buckets, hash__in=hashes):
            transactions.append(transaction.as_json())

        return transactions

    @classmethod
    def get(cls, bucket, hash):
        try:
            transaction = Transaction.objects.get(bucket=bucket, hash=hash)
            return transaction.as_json()
        except DoesNotExist:
            return None

    @classmethod
    def from_address(cls, address):
        address_meta = Address.get(address)

        if not address_meta:
            return list()

        return Transaction.filter(
            buckets=[transaction['bucket'] for transaction in address_meta['transactions']],
            hashes=[transaction['hash'] for transaction in address_meta['transactions']]
        )

    @classmethod
    def from_transaction_hash(cls, hash):
        transaction_meta = TransactionHash.get(hash)

        if not transaction_meta:
            return None

        return Transaction.get(transaction_meta['bucket'], transaction_meta['hash'])

    @classmethod
    def from_bundle_hash(cls, bundle):
        bundle_meta = Bundle.get(bundle)

        if not bundle_meta:
            return list()

        return Transaction.filter(
            buckets=[transaction['bucket'] for transaction in bundle_meta['transactions']],
            hashes=[transaction['hash'] for transaction in bundle_meta['transactions']]
        )

    def as_json(self):
        return {
            "hash": self.hash,
            "address": self.address,
            "value": self.value,
            "timestamp": self.transaction_time,
            "signature_message_fragment": self.signature_message_fragment,
            "tag": self.tag,
            "tag_index": self.tag_index,
            "current_index": self.current_index,
            "last_index": self.last_index,
            "bundle": self.bundle,
            "trunk_transaction_hash": self.trunk_transaction_hash,
            "branch_transaction_hash": self.branch_transaction_hash,
            "nonce": self.nonce,
            "min_weight_magnitude": self.min_weight_magnitude,
            "persistence": self.persistence
        }


class Bundle(Base):
    __table_name__ = 'bundles'

    bucket = columns.Text(primary_key=True, partition_key=True, required=True)
    bundle = columns.Text(primary_key=True, required=True)
    transactions = columns.List(columns.UserDefinedType(TransactionObject))

    @classmethod
    def get(cls, bundle):
        try:
            bundle = Bundle.objects.get(bucket=bundle[:5], bundle=bundle)
            return bundle.as_json()
        except DoesNotExist:
            return None

    def as_json(self):
        return {
            'bundle': self.bundle,
            'transactions': self.transactions
        }


class Tag(Base):
    __table_name__ = 'tags'

    bucket = columns.Text(primary_key=True, partition_key=True, required=True)
    tag = columns.Text(primary_key=True, required=True)
    transactions = columns.List(columns.UserDefinedType(TransactionObject))

    @classmethod
    def get_transaction_hashes(cls, tag):
        tag_meta = Tag.get(tag)

        if not tag_meta:
            return list()

        return [transaction['hash'] for transaction in tag_meta['transactions']]

    @classmethod
    def get(cls, tag):
        try:
            tag = Tag.objects.get(bucket=tag[:5], tag=tag)
            return tag.as_json()
        except DoesNotExist:
            return None

    def as_json(self):
        return {
            'tag': self.tag,
            'transactions': self.transactions
        }


class TransactionHash(Base):
    __table_name__ = 'transaction_hashes'

    bucket = columns.Text(primary_key=True, partition_key=True, required=True)
    hash = columns.Text(primary_key=True, required=True)
    date = columns.Text(required=True)

    @classmethod
    def get(cls, hash):
        try:
            transaction = TransactionHash.objects.get(bucket=hash[:5], hash=hash)
            return transaction.as_json()
        except DoesNotExist:
            return None

    def as_json(self):
        return {
            'hash': self.hash,
            'bucket': self.date
        }


class Address(Base):
    __table_name__ = 'addresses'

    bucket = columns.Text(primary_key=True, partition_key=True, required=True)
    address = columns.Text(primary_key=True, required=True)
    transactions = columns.List(columns.UserDefinedType(TransactionObject))

    @classmethod
    def get(cls, address):
        try:
            address = Address.objects.get(bucket=address[:5], address=address)
            return address.as_json()
        except DoesNotExist:
            return None

    def as_json(self):
        return {
            'address': self.address,
            'transactions': self.transactions
        }


class Approvee(Base):
    __table_name__ = 'approvees'

    bucket = columns.Text(primary_key=True, partition_key=True, required=True)
    hash = columns.Text(primary_key=True, required=True)
    approvees = columns.List(columns.UserDefinedType(TransactionObject))

    @classmethod
    def get(cls, hash):
        try:
            approvee = Approvee.objects.get(bucket=hash[:5], hash=hash)
            return approvee.as_json()
        except DoesNotExist:
            return None

    def as_json(self):
        return {
            'hash': self.hash,
            'transactions': self.transactions
        }

    @classmethod
    def get_approvees_hashes(cls, hash):
        approvee_meta = Approvee.get(hash)

        if not approvee_meta:
            return list()

        return [transaction['hash'] for transaction in approvee_meta['approvees']]
