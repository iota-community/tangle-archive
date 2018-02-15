"""

Usage:
  store.py [-e <env>]

Options:
    -e  --env <env>
      Name of environment that will be used.

"""
import sys
from schema import Transaction, Address, Tag,\
    Bundle, Approvee
from docopt import docopt
from cassandra.cqlengine.management import sync_table
from cassandra.cqlengine import connection
from cassandra.cqlengine.query import LWTException

connection.setup(['127.0.0.1'], 'cqlengine', protocol_version=3)

print sys.maxsize


class Index:
    def __init__(self):
        self.bundles = {}
        self.addresses = {}
        self.tags = {}
        self.hashes_with_approvees = {}
        self.transactions = Transaction.objects.limit(None)

        self.initialize()

    def initialize(self):
        print len(self.transactions)
        for idx, tx in enumerate(self.transactions):
            self.map_bundles(tx)
            self.map_addresses(tx)
            self.map_tags(tx)
            self.map_approvees(tx)

            print idx
            print self.hashes_with_approvees

    def map_bundles(self, tx):
        if tx.bundle not in self.bundles:
            self.bundles[tx.bundle] = list()

        self.bundles[tx.bundle].append(tx.hash)

    def map_addresses(self, tx):
        if tx.address not in self.addresses:
            self.addresses[tx.address] = list()

        self.addresses[tx.address].append(tx.hash)

    def map_tags(self, tx):
        if tx.tag not in self.tags:
            self.tags[tx.tag] = list()

        self.tags[tx.tag].append(tx.hash)

    def map_approvees(self, tx):
        self.hashes_with_approvees[tx.hash] = set([
            t.hash for t in self.transactions if t.branch_transaction_hash == tx.hash or
                                                 t.trunk_transaction_hash == tx.hash
        ])

if __name__ == '__main__':
    Index()
