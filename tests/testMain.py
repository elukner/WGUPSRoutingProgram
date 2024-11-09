import unittest
from unittest.mock import patch, mock_open
from HashTable import *
from Package import *
from main import *

class MainTestCase(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data="packageID,deliveryAddress,city,state,zip,deliveryDeadline,packageWeight,pageSpecialNotes\n1,195 W Oakland Ave,Salt Lake City,UT,84115,10:30 AM,21,Handle with care\n2,2530 S 500 E,Salt Lake City,UT,84106,EOD,44,Leave at front door\n")
    def testLoadPackageData(self, mock_file):
            # Arrange
            hashTable = HashTable()

            # Act
            loadPackageData("packageCSV.csv", hashTable)

            # Assert
            # Verify that the package was inserted into the hash table
            package1 = hashTable.lookUp(1)
            package2 = hashTable.lookUp(2)

            self.assertIsNotNone(package1)
            self.assertIsNotNone(package2)

            # Verify the contents of the first package
            self.assertEqual(package1.packageID, 1)
            self.assertEqual(package1.deliveryAddress, "195 W Oakland Ave")
            self.assertEqual(package1.city, "Salt Lake City")
            self.assertEqual(package1.state, "UT")
            self.assertEqual(package1.zip, "84115")
            self.assertEqual(package1.deliveryDeadline, "10:30 AM")
            self.assertEqual(package1.packageWeight, "21")
            self.assertEqual(package1.pageSpecialNotes, "Handle with care")
            self.assertEqual(package1.deliveryStatus, "At Hub")

            # Verify the contents of the second package
            self.assertEqual(package2.packageID, 2)
            self.assertEqual(package2.deliveryAddress, "2530 S 500 E")
            self.assertEqual(package2.city, "Salt Lake City")
            self.assertEqual(package2.state, "UT")
            self.assertEqual(package2.zip, "84106")
            self.assertEqual(package2.deliveryDeadline, "EOD")
            self.assertEqual(package2.packageWeight, "44")
            self.assertEqual(package2.pageSpecialNotes, "Leave at front door")
            self.assertEqual(package2.deliveryStatus, "At Hub")

    def testLoadDistanceData(self):
        self.assertEqual(True, False)  # add assertion here

    def testLoadAddressData(self):
        self.assertEqual(True, False)  # add assertion here

    def testPrintUI(self):
        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()
