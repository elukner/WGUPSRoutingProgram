import unittest
from unittest.mock import mock_open, patch
from io import StringIO

from CSV import loadAddressData, loadDistanceData, loadPackageData, distanceBetween, minDistanceFrom
from HashTable import HashTable
from Package import Package


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

    def setUp(self):
        # Set up mock data for addressData and distanceData
        global addressData, distanceData

        addressData = [
            "4001 South 700 East",
            "1060 Dalton Ave S",
            "1330 2100 S"
        ]

        distanceData = [
            [0.0, 7.2, 3.8],
            [7.2, 0.0, 4.4],
            [3.8, 4.4, 0.0]
        ]

    def test_distance_between_valid_addresses(self):
        # Test distance between two valid addresses
        distance = distanceBetween('4001 South 700 East', '1060 Dalton Ave S')
        self.assertEqual(distance, 7.2)

        distance = distanceBetween('1060 Dalton Ave S', '1330 2100 S')
        self.assertEqual(distance, 4.4)

    def test_distance_between_same_address(self):
        # Test distance between the same address (should be 0)
        distance = distanceBetween("4001 South 700 East", "4001 South 700 East")
        self.assertEqual(distance, 0.0)

    def test_distance_between_invalid_addresses(self):
        # Test distance between invalid address (should return inf)
        distance = distanceBetween("Invalid Address", "1060 Dalton Ave S")
        self.assertEqual(distance, float('inf'))

        distance = distanceBetween("4001 South 700 East", "Another Invalid Address")
        self.assertEqual(distance, float('inf'))

    def setUp(self):
        # Set up the mock data for testing
        global distanceData, addressData
        distanceData = [
            [0, 3, 5],
            [3, 0, 4],
            [5, 4, 0]
        ]
        addressData = ["Address A", "Address B", "Address C"]

        # Create some package objects
        self.package1 = Package(1, "Address B")
        self.package2 = Package(2, "Address C")
        self.truckPackages = [self.package1, self.package2]

    def test_min_distance_from(self):
        # Run minDistanceFrom to find the closest package
        closest_package = minDistanceFrom("Address A", self.truckPackages)
        # Assert that the closest package ID is as expected (closest to "Address A" is package 1)
        self.assertEqual(closest_package.packageID, 1)

    def test_empty_truck_packages(self):
        # Test the function with an empty list of truck packages
        closest_package = minDistanceFrom("Address A", [])
        # Assert that it returns None
        self.assertIsNone(closest_package)


if __name__ == '__main__':
    unittest.main()
