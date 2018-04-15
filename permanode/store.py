from __future__ import print_function
import sys

import datetime
import os
import transaction
from permanode.models import Transaction, Address, Tag,\
    Bundle, Approvee, TransactionObject, TransactionHash
from cassandra.cqlengine.query import LWTException


folder = './dumps/'


class Store:
    def __init__(self):
        self.extract_dump()

    def store_to_transactions_table(self, tx, date, persistence=False):
        try:
            return Transaction.if_not_exists().create(
                bucket=date,
                address=tx.address,
                value=tx.value,
                transaction_time=tx.timestampDate,
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
                min_weight_magnitude=tx.min_weight_magnitude,
                persistence=persistence
            )

        except LWTException as e:
            print(e, file=sys.stdout)

    def store_to_addresses_table(self, tx, date):
        try:
            return Address.if_not_exists().create(
                bucket=tx.address[:5],
                address=tx.address,
                transactions=[
                    TransactionObject(
                        hash=tx.hash,
                        bucket=date
                    )
                ]
            )
        except LWTException:
            pass
        try:
            return Address.objects(bucket=tx.address[:5], address=tx.address).update(
                transactions__append=[
                    TransactionObject(
                        hash=tx.hash,
                        bucket=date
                    )]
            )
        except LWTException:
            raise Exception('Could not update address.')

    def store_to_tags_table(self, tx, date):
        try:
            return Tag.if_not_exists().create(
                bucket=tx.tag[:5],
                tag=tx.tag,
                transactions=[
                    TransactionObject(
                        hash=tx.hash,
                        bucket=date
                    )
                ]
            )
        except LWTException:
            pass
        try:
            return Tag.objects(bucket=tx.tag[:5], tag=tx.tag).update(
                transactions__append=[
                    TransactionObject(
                        hash=tx.hash,
                        bucket=date
                )]
            )
        except LWTException:
            raise Exception('Could not update tag.')

    def store_to_bundles_table(self, tx, date):
        try:
            return Bundle.if_not_exists().create(
                bucket=tx.bundle_hash[:5],
                bundle=tx.bundle_hash,
                transactions=[
                    TransactionObject(
                        hash=tx.hash,
                        bucket=date
                )]
            )
        except LWTException:
            pass
        try:
            return Bundle.objects(bucket=tx.bundle_hash[:5], bundle=tx.bundle_hash).update(
                transactions__append=[
                    TransactionObject(
                        hash=tx.hash,
                        bucket=date
                )]
            )
        except LWTException:
            raise Exception('Could not update bundle.')

    def store_to_transaction_hashes_table(self, tx, date):
        try:
            return TransactionHash.if_not_exists().create(
                bucket=tx.hash[:5],
                hash=tx.hash,
                date=date
            )
        except LWTException:
            print('Transaction hash already dumped', file=sys.stdout)

    def store_to_approvee_table(self, hash, hash_ref, date):
        try:
            return Approvee.if_not_exists().create(
                bucket=hash_ref[:5],
                hash=hash_ref,
                approvees=[
                    TransactionObject(
                        hash=hash,
                        bucket=date
                )]
            )
        except LWTException:
            pass
        try:
            return Approvee.objects(bucket=hash_ref[:5], hash=hash_ref).update(
                approvees__append=[
                    TransactionObject(
                        hash=hash,
                        bucket=date
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
                            tx.timestamp
                        ).strftime('%Y-%m-%d-%H')

                        self.store_to_transactions_table(tx, date)
                        self.store_to_addresses_table(tx, date)
                        self.store_to_bundles_table(tx, date)
                        self.store_to_tags_table(tx, date)
                        self.store_to_transaction_hashes_table(tx, date)
                        self.store_to_approvee_table(hash, branch, date)
                        self.store_to_approvee_table(hash, trunk, date)

                        count += 1
                        print('Dumped so far', count, file=sys.stdout)


