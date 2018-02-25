from __future__ import print_function
import sys

from cassandra.cqlengine import columns
from cassandra.cqlengine.usertype import UserType
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

    @classmethod
    def from_tag(cls, tag):
        tag_meta = Tag.get(tag)

        if not tag_meta:
            return list()

        return Transaction.filter(
            buckets=[transaction['bucket'] for transaction in tag_meta['transactions']],
            hashes=[transaction['hash'] for transaction in tag_meta['transactions']]
        )

    @classmethod
    def filter(cls, buckets=list(), hashes=list()):
        transactions = list()

        for transaction in Transaction.objects.filter(bucket__in=buckets, hash__in=hashes):
            transactions.append(transaction.as_json())

        return transactions

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
            "persistence": True  # since all txs from db are confirmed
        }


class Bundle(Base):
    __table_name__ = 'bundles'

    bucket = columns.Text(primary_key=True, partition_key=True, required=True)
    bundle = columns.Text(primary_key=True, required=True)
    transactions = columns.List(columns.UserDefinedType(TransactionObject))


class Tag(Base):
    __table_name__ = 'tags'

    bucket = columns.Text(primary_key=True, partition_key=True, required=True)
    tag = columns.Text(primary_key=True, required=True)
    transactions = columns.List(columns.UserDefinedType(TransactionObject))

    @classmethod
    def get(cls, tag):
        tag = Tag.objects.get(bucket=tag[:5], tag=tag)

        return tag.as_json()

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

class Address(Base):
    __table_name__ = 'addresses'

    bucket = columns.Text(primary_key=True, partition_key=True, required=True)
    address = columns.Text(primary_key=True, required=True)
    transactions = columns.List(columns.UserDefinedType(TransactionObject))


class Approvee(Base):
    __table_name__ = 'approvees'

    bucket = columns.Text(primary_key=True, partition_key=True, required=True)
    hash = columns.Text(primary_key=True, required=True)
    approvees = columns.List(columns.UserDefinedType(TransactionObject))
