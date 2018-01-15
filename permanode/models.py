from cassandra.cqlengine import columns
from permanode import db


class Base(db.Model):
    __abstract__ = True
    __keyspace__ = "permanode"


class AddressTokenReceivedModel(Base):
    __table_name__ = "table_tokens_revieved_by_address"
    address = columns.Text(primary_key=True)
    total_tokens_received = columns.Counter()

    def get_data(self):
        return {
            "total_tokens_received": self.total_tokens_received
        }


class TransactionModel(Base):
    __table_name__ = "transactions"

    id = columns.Text(primary_key=True)
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

    def as_json(self):
        return {
            "id": self.id,
            "address": self.address,
            "value": self.value,
            "timestamp": self.transaction_time,
            "hash": self.hash,
            "signature_message_format": self.signature_message_fragment,
            "tag": self.tag,
            "tag_index": self.tag_index,
            "current_index": self.current_index,
            "last_index": self.last_index,
            "bundle_hash": self.bundle_hash,
            "trunk_transaction_hash": self.trunk_transaction_hash,
            "branch_transaction_hash": self.branch_transaction_hash,
            "nonce": self.nonce
        }


class TransactionHashModel(Base):
    __table_name__ = 'transaction_hash'

    hash = columns.Text(primary_key=True)
    id = columns.Text(primary_key=True)

    def as_json(self):
        return {
            "id": self.id,
            "hash": self.hash
        }


class BundleHashModel(Base):
    __table_name__ = 'bundle_hash'

    bundle_hash = columns.Text(primary_key=True)
    id=columns.Text(primary_key=True)

    def as_json(self):
        return {
            "id": self.id,
            "bundle_hash": self.bundle_hash
        }


class TagModel(Base):
    __table_name__ = 'tag'

    tag = columns.Text(primary_key=True)
    id=columns.Text(primary_key=True)

    def as_json(self):
        return {
            "id": self.id,
            "tag": self.tag
        }


class AddressModel(Base):
    __table_name__ = 'address'

    address = columns.Text(primary_key=True)
    id=columns.Text(primary_key=True)

    def as_json(self):
        return {
            "id": self.id,
            "address": self.address
        }