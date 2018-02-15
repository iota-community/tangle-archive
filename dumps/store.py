"""

Usage:
  store.py [-e <env>]

Options:
    -e  --env <env>
      Name of environment that will be used.

"""


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


def is_development(env):
    return env is 'development'


def create_connection(env):
    if is_development(env):
        connection.setup(['127.0.0.1'], 'cqlengine', protocol_version=3)
    else:
        connection.setup(
           ['127.0.0.1'],
           'cqlengine',
           protocol_version=3,
           ssl_options={
                'ca_certs': '../certs/rootCa.crt'
           }
        )


def sync_tables():
    sync_table(Transaction)
    sync_table(Address)


class Store:
    def __init__(self):
        self.extract_dump()

    def store_to_transactions_table(self, tx):
        try:
            Transaction.if_not_exists().create(
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

    def store_branch_hash(self, tx):
        try:
            Transaction.if_not_exists().create(
                hash=tx.branch_transaction_hash
            )

        except LWTException as e:
            print e

        return self

    def store_trunk_hash(self, tx):
        try:
            Transaction.if_not_exists().create(
                hash=tx.trunk_transaction_hash
            )

        except LWTException as e:
            print e

        return self

    def store_to_address_table(self, tx):
        try:
            Address.objects(address=tx.address).update(
                hashes__add={tx.hash}
            )

        except LWTException as e:
            print e

        return self

    def update_transaction_with_this_branch(self, tx):
        try:
            transaction_obj = Transaction.objects(tx.branch).filter(
                hash=tx.branch_transaction_hash
            )

            if transaction_obj:
                Transaction.objects(hash=tx.branch_transaction_hash).update(
                    approvees__add={tx.hash}
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


                        self.store_to_address_table(tx)

                        count += 1
                        print 'Dumped so far', count


if __name__ == '__main__':
    arguments = docopt(__doc__)
    allowed_envs = ['development', 'production']

    current_env = None
    specified_env = arguments['<env>']

    if specified_env not in allowed_envs:
        current_env = 'development'
    else:
        current_env = specified_env

    create_connection(current_env)
    sync_tables()
    Store()
