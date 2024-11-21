import unittest
from unittest.mock import mock_open, patch
from io import StringIO

from CSV import loadAddressData, loadDistanceData, loadPackageData
from HashTable import HashTable


class CSVTestCase(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open, read_data="0.0,7.1,3.8\n7.1,0.0,7.5\n3.8,7.5,0.0")
    def test_loadDistanceData(self, mock_file):
        # Test loadDistanceData function
        global distanceData
        distanceData = []  # Reset the global distanceData before running the test

        fileName = "distanceCSV.csv"
        result = loadDistanceData(fileName)

        expected = [
            [0.0, 7.1, 3.8],
            [7.1, 0.0, 7.5],
            [3.8, 7.5, 0.0]
        ]

        self.assertEqual(result, expected)
        mock_file.assert_called_once_with(fileName)

    @patch("builtins.open", new_callable=mock_open,
           read_data="0,Western Governors University,4001 South 700 East\n1,International Peace Gardens,1060 Dalton Ave S")
    def test_loadAddressData(self, mock_file):
        # Test loadAddressData function
        global addressData
        addressData = []  # Reset the global addressData before running the test

        fileName = "addressCSV.csv"
        result = loadAddressData(fileName)

        expected = [
            "4001 South 700 East",
            "1060 Dalton Ave S"
        ]

        self.assertEqual(result, expected)
        mock_file.assert_called_once_with(fileName)

    @patch("builtins.open", new_callable=mock_open,
           read_data="1,195 W Oakland Ave,Salt Lake City,UT,84115,10:30 AM,21\n2,2530 S 500 E,Salt Lake City,UT,84106,EOD,44")
    def test_loadPackageData(self, mock_file):
        # Test loadPackageData function
        hashTable = HashTable()

        fileName = "packageCSV.csv"
        loadPackageData(fileName, hashTable)

        # Verify that the packages are correctly loaded into the hash table
        package_1 = hashTable.lookUp(1)
        package_2 = hashTable.lookUp(2)

        self.assertIsNotNone(package_1)
        self.assertEqual(package_1.packageID, 1)
        self.assertEqual(package_1.deliveryAddress, "195 W Oakland Ave")
        self.assertEqual(package_1.city, "Salt Lake City")
        self.assertEqual(package_1.state, "UT")
        self.assertEqual(package_1.zip, "84115")
        self.assertEqual(package_1.deliveryDeadline, "10:30 AM")
        self.assertEqual(package_1.packageWeight, 21)

        self.assertIsNotNone(package_2)
        self.assertEqual(package_2.packageID, 2)
        self.assertEqual(package_2.deliveryAddress, "2530 S 500 E")
        self.assertEqual(package_2.city, "Salt Lake City")
        self.assertEqual(package_2.state, "UT")
        self.assertEqual(package_2.zip, "84106")
        self.assertEqual(package_2.deliveryDeadline, "EOD")
        self.assertEqual(package_2.packageWeight, 44)

        mock_file.assert_called_once_with(fileName)


if __name__ == '__main__':
    unittest.main()
