import csv
import math

class HashTable:
    """
    This class represents a HashTable data structure for storing and managing package data.
    It supports inserting, looking up, removing, and retrieving all items in the hash table.
    """

    def __init__(self, initialCapacity=40):
        """
        Initialize the hash table with empty buckets
        :param initialCapacity: There is a maximum of 40 packages
        """
        self.table = []
        for i in range(initialCapacity):
            self.table.append([])

    def insert(self, key, item):
        """
        Inserts an item into the hash table.
        :param key: The unique identifier for the package (packageID).
        :param item: The package object to be stored in the hash table.
        :return: True if the item was successfully inserted or updated, False otherwise.
        """
        index = hash(key) % len(self.table)
        index_list = self.table[index]

        for kV in index_list:
            if kV[0] == key:
                kV[1] = item
                return True

        keyValue = [key, item]
        index_list.append(keyValue)
        return True

    def lookUp(self, key):
        """
        Searches for a key and returns its value.
        :param key: The unique identifier for the package (packageID).
        :return: The package object if found, otherwise None.
        """
        index = hash(key) % len(self.table)
        index_list = self.table[index]

        for kV in index_list:
            if kV[0] == key:
                return kV[1]
        return None

    def remove(self, key):
        """
        Removes a key from the hash table.
        :param key: The unique identifier for the package (packageID) to be removed.
        :return: None.
        """
        index = hash(key) % len(self.table)
        indexList = self.table[index]

        for kV in indexList:
            if kV[0] == key:
                indexList.remove(kV)

    def getAllItems(self):
        """
        Retrieves all items from the hash table.
        :return: A list of all package objects in the hash table.
        """
        allItems = []
        for bucket in self.table:
            for kV in bucket:
                allItems.append(kV[1])
        return allItems
