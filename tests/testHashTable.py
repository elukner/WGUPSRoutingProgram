import unittest

from HashTable import HashTable


class HashTableTestCase(unittest.TestCase):
    def setUp(self):
        # Create a hash table instance for testing
        self.hash_table = HashTable(initial_capacity=10)

    def testInsertNewItem(self):
        # Insert a new item into the hash table
        result = self.hash_table.insert(1, "Package 1")

        # Verify that the insert operation was successful
        self.assertTrue(result)

        # Verify that the item is in the correct bucket of the hash table
        index = hash(1) % len(self.hash_table.table)
        index_list = self.hash_table.table[index]
        self.assertIn([1, "Package 1"], index_list)

    def testUpdateExistingItem(self):
        # Insert a new item
        self.hash_table.insert(1, "Package 1")
        # Update the existing item with a new value
        result = self.hash_table.insert(1, "Updated Package 1")

        # Verify that the update operation was successful
        self.assertTrue(result)

        # Verify that the item has been updated in the hash table
        index = hash(1) % len(self.hash_table.table)
        index_list = self.hash_table.table[index]
        self.assertIn([1, "Updated Package 1"], index_list)
        # Ensure that the old value is no longer in the bucket
        self.assertNotIn([1, "Package 1"], index_list)

    def testInsertMultipleItems(self):
        # Insert multiple items with different keys
        self.hash_table.insert(1, "Package 1")
        self.hash_table.insert(2, "Package 2")
        self.hash_table.insert(3, "Package 3")

        # Verify that all items are inserted properly in their respective buckets
        index_1 = hash(1) % len(self.hash_table.table)
        index_2 = hash(2) % len(self.hash_table.table)
        index_3 = hash(3) % len(self.hash_table.table)

        self.assertIn([1, "Package 1"], self.hash_table.table[index_1])
        self.assertIn([2, "Package 2"], self.hash_table.table[index_2])
        self.assertIn([3, "Package 3"], self.hash_table.table[index_3])


    def testLookUp(self):
        self.assertEqual(True, False)  # add assertion here

    def testUpdate(self):
        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()
