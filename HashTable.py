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
# TODO + lookUp(self, key)
# B.  Develop a look-up function that takes the package ID as input and returns
# each of the following corresponding data components:
# delivery address
# delivery deadline
# delivery city
# delivery zip code
# package weight
# delivery status (i.e., at the hub, en route, or delivered), including the delivery time

class HashTable:
    # Constructor to initialize the hash table, with an optional parameter for the initial capacity.
    def __init__(self, initialCapacity=40):
        # Create the hash table with empty bucket lists, each bucket represented by an empty list.
        self.table = []
        for i in range(initialCapacity):
            self.table.append([])

    def insert(self, key, item):
        '''
        function inserts a new item and updates items
        :param key: packageID
        :param item: package object
        :return: boolean
        '''
        index = hash(key) % len(self.table)
        index_list = self.table[index]

        #updates key if it exists already in index
        for kV in index_list:
            #print(key_value) TODO delete later?
            if kV[0] == key:
                kV[1] = item
                return True

        #if key does not exist already in index
        keyValue = [key, item]
        index_list.append(keyValue)
        return True

    def lookUp(self, key):
        '''
        function searches for a key and returns its value
        :param key: packageID
        :return: package object
        '''
        index = hash(key) % len(self.table)
        index_list = self.table[index]
        #print(index_list) TODO delete later?

        #searches for the key in the index_list
        for kV in index_list:
            #print(key_value) TODO delete later?
            if kV[0] == key:
                return kV[1] #this is the value
        return None

    def remove(self, key):
        """
        function removes a key from the table
        :param key:
        :return:
        """
        index = hash(key) % len(self.table)
        indexList = self.table[index]

        for kV in indexList:
            if kV[0] == key:
                indexList.remove([kV[0], kV[1]])


    def getAllItems(self):
        '''
        Function retrieves all the items from the hash table.
        :return: A list of all items in the hash table.
        '''
        allItems = []
        for bucket in self.table:
            for kV in bucket:
                allItems.append(kV[1])  # Appending the value (package object)
        return allItems



