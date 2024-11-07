import csv
import math

#TODO 1-Create HashTable data structure
class HashTable:
    # Constructor to initialize the hash table, with an optional parameter for the initial capacity.
    def __init__(self, initial_capacity=40):
        # Create the hash table with empty bucket lists, each bucket represented by an empty list.
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])

#TODO + insert(key, item)
    def insert(self, key, item):
        pass #TODO delete later

#TODO + lookUp(self, key)
    def lookUp(self, key):
        pass #TODO delete later

#TODO + update(self, key, item)
    def update(self, key, item):
        pass #TODO delete later

