import datetime
import os
import transaction
from schema import Transaction, Address, Tag,\
    Bundle, Approvee, TransactionObject, TransactionHash, KEYSPACE
from cassandra.cqlengine.management import sync_table, sync_type
from cassandra.cqlengine import connection
from cassandra.cqlengine.query import LWTException


folder = './'


def create_connection():
    connection.setup(['127.0.0.1'], 'cqlengine', protocol_version=3)


def sync_tables():
    sync_table(Transaction)
    sync_table(Address)
    sync_table(Tag)
    sync_table(Bundle)
    sync_table(TransactionHash)
    sync_table(Approvee)

def sync_types():
    sync_type(KEYSPACE, TransactionObject)

class Store:
    def __init__(self):
        self.extract_dump()

    def store_to_transactions_table(self, tx, date):
        try:
            return Transaction.if_not_exists().create(
                bucket=date,
                address=tx.address,
                value=tx.value,
                transaction_time=tx.timestamp,
                hash=tx.hash,
                signature_message_fragment=tx.signature_message_fragment,
                tag=tx.tag,
                tag_index=tx.tagIndex,
                current_index=tx.current_index,
                last_index=tx.last_index,
                bundle=tx.bundle_hash,
                trunk_transaction_hash=tx.trunk_transaction_hash,
                branch_transaction_hash=tx.branch_transaction_hash,
                nonce=tx.nonce,
                min_weight_magnitude=tx.min_weight_magnitude
            )

        except LWTException as e:
            print e

    def store_to_addresses_table(self, tx, date):
        try:
            return Address.if_not_exists().create(
                bucket=tx.address[:10],
                address=tx.address,
                hashes=[
                    TransactionObject(
                        hash=tx.hash,
                        date=date
                    )
                ]
            )
        except LWTException:
            pass
        try:
            return Address.objects(bucket=tx.address[:10], address=tx.address).update(
                hashes__append=[
                    TransactionObject(
                        hash=tx.hash,
                        date=date
                    )]
            )
        except LWTException:
            raise Exception('Could not update address.')

    def store_to_tags_table(self, tx, date):
        try:
            return Tag.if_not_exists().create(
                bucket=tx.tag[:10],
                tag=tx.tag,
                hashes=[
                    TransactionObject(
                        hash=tx.hash,
                        date=date
                    )
                ]
            )
        except LWTException:
            pass
        try:
            return Tag.objects(bucket=tx.tag[:10], tag=tx.tag).update(
                hashes__append=[
                    TransactionObject(
                        hash=tx.hash,
                        date=date
                )]
            )
        except LWTException:
            raise Exception('Could not update tag.')

    def store_to_bundles_table(self, tx, date):
        try:
            return Bundle.if_not_exists().create(
                bucket=tx.bundle_hash[:10],
                bundle=tx.bundle_hash,
                hashes=[
                    TransactionObject(
                        hash=tx.hash,
                        date=date
                )]
            )
        except LWTException:
            pass
        try:
            return Bundle.objects(bucket=tx.bundle_hash[:10], bundle=tx.bundle_hash).update(
                hashes__append=[
                    TransactionObject(
                        hash=tx.hash,
                        date=date
                )]
            )
        except LWTException:
            raise Exception('Could not update bundle.')

    def store_to_transaction_hashes_table(self, tx, date):
        try:
            return TransactionHash.if_not_exists().create(
                bucket=tx.hash[:10],
                hash=tx.hash,
                date=date
            )
        except LWTException:
            print 'Transaction hash already dumped.'

    def store_to_approvee_table(self, hash, hash_ref, date):
        try:
            return Approvee.if_not_exists().create(
                bucket=hash_ref[:10],
                hash=hash_ref,
                approvees=[
                    TransactionObject(
                        hash=hash,
                        date=date
                )]
            )
        except LWTException:
            pass
        try:
            return Approvee.objects(bucket=hash_ref[:10], hash=hash_ref).update(
                approvees__append=[
                    TransactionObject(
                        hash=hash,
                        date=date
                )]
            )
        except LWTException:
            raise Exception('Could not update approvee.')

    def extract_dump(self):
        for file in sorted(os.listdir(folder)):
            if file.endswith('.dmp'):
                count = 0
                with open(folder + file, 'r') as f:
                    for line in f:
                        tx_hash, tx = line.split(',')
                        tx = transaction.transaction(tx, tx_hash)

                        hash = tx.hash
                        branch = tx.branch_transaction_hash
                        trunk = tx.trunk_transaction_hash

                        date = datetime.datetime.fromtimestamp(
                               int(tx.timestamp)
                            ).strftime('%Y-%m-%d')

                        self.store_to_transactions_table(tx, date)
                        self.store_to_addresses_table(tx, date)
                        self.store_to_bundles_table(tx, date)
                        self.store_to_tags_table(tx, date)
                        self.store_to_transaction_hashes_table(tx, date)
                        self.store_to_approvee_table(hash, branch, date)
                        self.store_to_approvee_table(hash, trunk, date)

                        count += 1
                        print 'Dumped so far', count


if __name__ == '__main__':
    create_connection()
    sync_tables()
    sync_types()
    Store()
