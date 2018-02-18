import datetime
import os
import transaction
from schema import Transaction, Address, Tag,\
    Bundle, Approvee
from cassandra.cqlengine.management import sync_table
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
    sync_table(Approvee)


class Store:
    def __init__(self):
        self.extract_dump()

    def store_to_transactions_table(self, tx, date):
        try:
            Transaction.if_not_exists().create(
                date=date,
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

        return self

    def store_to_addresses_table(self, tx):
        try:
            Address.if_not_exists().create(
                address=tx.address,
                hashes=[tx.hash]
            )
        except LWTException as e:
            print 'Already has an address. Will update hashes'
            Address.objects(address=tx.address).update(
                hashes__add={tx.hash}
            )

        return self

    def store_to_tags_table(self, tx):
        try:
            Tag.if_not_exists().create(
                tag=tx.tag,
                hashes=[tx.hash]
            )
        except LWTException as e:
            print 'Already has a tag. Will update hashes'
            Tag.objects(tag=tx.tag).update(
                hashes__add={tx.hash}
            )

        return self

    def store_to_bundles_table(self, tx):
        try:
            Bundle.if_not_exists().create(
                bundle=tx.bundle_hash,
                hashes=[tx.hash]
            )
        except LWTException as e:
            print 'Already has a bundle. Will update hashes'
            Bundle.objects(bundle=tx.bundle_hash).update(
                hashes__add={tx.hash}
            )

        return self

    def store_to_approvee_table(self, hash, hash_ref):
        try:
            Approvee.if_not_exists().create(
                hash=hash_ref,
                approvees=[hash]
            )
        except LWTException as e:
            print 'Already has a ref. Will update hashes'
            Approvee.objects(hash=hash_ref).update(
                approvees__add={hash}
            )

        return self

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

                        self.store_to_transactions_table(tx, date)\
                            .store_to_addresses_table(tx)\
                            .store_to_bundles_table(tx)\
                            .store_to_tags_table(tx)\
                            .store_to_approvee_table(hash, branch)\
                            .store_to_approvee_table(hash, trunk)

                        count += 1
                        print 'Dumped so far', count


if __name__ == '__main__':
    create_connection()
    sync_tables()
    Store()
