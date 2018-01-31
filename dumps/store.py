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
from schema import TransactionHash, Transactions, Address, Tag,\
    BundleHash, TrunkTransactionHash, BranchTransactionHash
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
    sync_table(Transactions)
    sync_table(TransactionHash)
    sync_table(Address)
    sync_table(Tag)
    sync_table(BundleHash)
    sync_table(TrunkTransactionHash)
    sync_table(BranchTransactionHash)


class Store:
    def __init__(self):
        self.extract_dump()

    def store_to_transactions_table(self, _id, tx):
        try:
            Transactions.if_not_exists().create(
                id=_id,
                address=tx.address,
                value=tx.value,
                transaction_time=tx.timestamp,
                hash=tx.hash,
                signature_message_fragment=tx.signature_message_fragment,
                tag=tx.tag,
                tag_index=tx.tagIndex,
                current_index=tx.current_index,
                last_index=tx.last_index,
                bundle_hash=tx.bundle_hash,
                trunk_transaction_hash=tx.trunk_transaction_hash,
                branch_transaction_hash=tx.branch_transaction_hash,
                nonce=tx.nonce,
                min_weight_magnitude=tx.min_weight_magnitude
            )

        except LWTException as e:
            print e

        return self

    def store_to_transactions_hash_table(self, _id, tx):
        try:
            TransactionHash.if_not_exists().create(
                id=_id,
                hash=tx.hash
            )
        except LWTException as e:
            print e

        return self

    def store_to_branch_transaction_hash(self, _id, tx):
        try:
            BranchTransactionHash.if_not_exists().create(
                id=_id,
                branch=tx.branch_transaction_hash
            )
        except LWTException as e:
            print e

        return self

    def store_to_trunk_transaction_hash(self, _id, tx):
        try:
            TrunkTransactionHash.if_not_exists().create(
                id=_id,
                trunk=tx.trunk_transaction_hash
            )
        except LWTException as e:
            print e

        return self

    def store_to_bundle_hash_table(self, _id, tx):
        try:
            BundleHash.if_not_exists().create(
                id=_id,
                bundle_hash=tx.bundle_hash
            )
        except LWTException as e:
            print e

        return self

    def store_to_tag_table(self, _id, tx):
        try:
            Tag.if_not_exists().create(
                id=_id,
                tag=tx.tag
            )
        except LWTException as e:
            print e

        return self

    def store_to_address_table(self, _id, tx):
        try:
            Address.if_not_exists().create(
                id=_id,
                address=tx.address
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

                        _id = str(uuid.uuid4())

                        self.store_to_transactions_table(_id, tx)\
                            .store_to_transactions_hash_table(_id, tx)\
                            .store_to_address_table(_id, tx)\
                            .store_to_bundle_hash_table(_id, tx)\
                            .store_to_tag_table(_id, tx)\
                            .store_to_branch_transaction_hash(_id, tx)\
                            .store_to_trunk_transaction_hash(_id, tx)

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
