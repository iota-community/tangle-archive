import datetime
import os
import uuid
import transaction
from schema import Transaction, Address, Tag,\
    Bundle, Approvee
from docopt import docopt
from cassandra.cqlengine.management import sync_table
from cassandra.cqlengine import connection
from cassandra.cqlengine.query import LWTException


folder = './'


def create_connection():
    connection.setup(['127.0.0.1'], 'cqlengine', protocol_version=3)



def sync_tables():
    sync_table(Transaction)



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

    def extract_dump(self):
        for file in sorted(os.listdir(folder)):
            if file.endswith('.dmp'):
                count = 0
                with open(folder + file, 'r') as f:
                    for line in f:
                        tx_hash, tx = line.split(',')
                        tx = transaction.transaction(tx, tx_hash)

                        date = datetime.datetime.fromtimestamp(
                               int(tx.timestamp)
                            ).strftime('%Y-%m-%d')

                        self.store_to_transactions_table(tx, date)

                        count += 1
                        print 'Dumped so far', count


if __name__ == '__main__':
    create_connection()
    sync_tables()
    Store()
