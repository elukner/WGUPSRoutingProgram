import csv
import math


# TODO 1-Create HashTable data structure
# A.  Develop a hash table, without using any additional libraries or classes,
# that has an insertion function that takes the package ID as input and inserts
# each of the following data components into the hash table:
# delivery address
# delivery deadline
# delivery city
# delivery zip code
# package weight
# delivery status (i.e., at the hub, en route, or delivered), including the delivery time
class HashTable:
    # Constructor to initialize the hash table, with an optional parameter for the initial capacity.
    def __init__(self, initial_capacity=40):
        # Create the hash table with empty bucket lists, each bucket represented by an empty list.
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])

    # TODO + insert(key, item)
    def insert(self, key, item):
        pass  # TODO delete later

    # TODO + lookUp(self, key)
    # B.  Develop a look-up function that takes the package ID as input and returns
    # each of the following corresponding data components:
    # delivery address
    # delivery deadline
    # delivery city
    # delivery zip code
    # package weight
    # delivery status (i.e., at the hub, en route, or delivered), including the delivery time

    def lookUp(self, key):
        pass  # TODO delete later

    # TODO + update(self, key, item)
    def update(self, key, item):
        pass  # TODO delete later
