import unittest

from HashTable import HashTable


class HashTableTestCase(unittest.TestCase):
    def setUp(self):
        # Create a hash table instance for testing
        self.hashTable = HashTable(initialCapacity=40)

    def testInsertNewItem(self):
        # Insert a new item into the hash table
        result = self.hashTable.insert(1, "Package 1")

        # Verify that the insert operation was successful
        self.assertTrue(result)

        # Verify that the item is in the correct bucket of the hash table
        index = hash(1) % len(self.hashTable.table)
        indexList = self.hashTable.table[index]
        self.assertIn([1, "Package 1"], indexList)

    def testUpdateExistingItem(self):
        # Insert a new item
        self.hashTable.insert(1, "Package 1")
        # Update the existing item with a new value
        result = self.hashTable.insert(1, "Updated Package 1")

        # Verify that the update operation was successful
        self.assertTrue(result)

        # Verify that the item has been updated in the hash table
        index = hash(1) % len(self.hashTable.table)
        indexList = self.hashTable.table[index]
        self.assertIn([1, "Updated Package 1"], indexList)
        # Ensure that the old value is no longer in the bucket
        self.assertNotIn([1, "Package 1"], indexList)

    def testInsertMultipleItems(self):
        # Insert multiple items with different keys
        self.hashTable.insert(1, "Package 1")
        self.hashTable.insert(2, "Package 2")
        self.hashTable.insert(3, "Package 3")

        # Verify that all items are inserted properly in their respective buckets
        index1 = hash(1) % len(self.hashTable.table)
        index2 = hash(2) % len(self.hashTable.table)
        index3 = hash(3) % len(self.hashTable.table)

        self.assertIn([1, "Package 1"], self.hashTable.table[index1])
        self.assertIn([2, "Package 2"], self.hashTable.table[index2])
        self.assertIn([3, "Package 3"], self.hashTable.table[index3])


    def testLookUpExistingItem(self):
        # Insert an item into the hash table
        self.hashTable.insert(1, "Package 1")
        # Look up the inserted item
        result = self.hashTable.lookUp(1)

        # Verify that the correct value is returned
        self.assertEqual(result, "Package 1") # add assertion here

    def testLookupNonExistingItem(self):
        # Insert an item into the hash table
        self.hashTable.insert(1, "Package 1")
        # Look up a key that does not exist
        result = self.hashTable.lookUp(2)

        # Verify that None is returned for a non-existing key
        self.assertIsNone(result)

    def testLookupAfterUpdate(self):
        # Insert an item into the hash table
        self.hashTable.insert(1, "Package 1")
        # Update the item with the same key
        self.hashTable.insert(1, "Updated Package 1")
        # Look up the updated item
        result = self.hashTable.lookUp(1)

        # Verify that the updated value is returned
        self.assertEqual(result, "Updated Package 1")

    def testLookupMultipleItems(self):
        # Insert multiple items
        self.hashTable.insert(1, "Package 1")
        self.hashTable.insert(2, "Package 2")
        self.hashTable.insert(3, "Package 3")

        # Verify that each item can be correctly looked up
        self.assertEqual(self.hashTable.lookUp(1), "Package 1")
        self.assertEqual(self.hashTable.lookUp(2), "Package 2")
        self.assertEqual(self.hashTable.lookUp(3), "Package 3")


if __name__ == '__main__':
    unittest.main()
