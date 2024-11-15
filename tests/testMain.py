import unittest
from unittest.mock import patch, mock_open
from HashTable import *
from Package import *
from main import *
from Truck import Truck
from CSV import *

class MainTestCase(unittest.TestCase):
    def setUp(self):
        # Create a hash table (a mock or actual instance, depending on implementation)
        self.hashTable = {}

        # Create a truck object with a capacity of 3
        self.truck = Truck(truckId=1, hashTable=self.hashTable)

        # Mock packages
        self.package1 = Package(1, "195 W Oakland Ave", "Salt Lake City", "UT", "84115", "10:30 AM", 21, "")
        self.package2 = Package(2, "2530 S 500 E", "Salt Lake City", "UT", "84106", "EOD", 44, "")
        self.package3 = Package(3, "233 Canyon Rd", "Salt Lake City", "UT", "84103", "EOD", 2, "")
        self.package4 = Package(4, "430 State St", "Salt Lake City", "UT", "84111", "EOD", 10, "")

        # List of available packages to load
        self.packages = [self.package1, self.package2, self.package3, self.package4]

    def test_truck_load_packages(self):
        # Load the truck using the truckLoadPackages function
        truckLoadPackages(self.truck, self.packages)

        # Assertions to validate the loading process

        # Check that the truck's packages list length is equal to the capacity (3 in this case)
        self.assertEqual(len(self.truck.packages), self.truck.capacity)

        # Check that the correct packages were loaded into the truck
        loaded_package_ids = [pkg.packageID for pkg in self.truck.packages]
        self.assertIn(self.package1.packageID, loaded_package_ids)
        self.assertIn(self.package2.packageID, loaded_package_ids)
        self.assertIn(self.package3.packageID, loaded_package_ids)

        # Verify that no more than capacity packages are loaded
        self.assertLessEqual(len(self.truck.packages), self.truck.capacity)

        # Verify that the loaded packages are removed from the remaining list
        remaining_package_ids = [pkg.packageID for pkg in self.packages if pkg not in self.truck.packages]
        self.assertNotIn(self.package1.packageID, remaining_package_ids)
        self.assertNotIn(self.package2.packageID, remaining_package_ids)
        self.assertNotIn(self.package3.packageID, remaining_package_ids)

    def test_no_infinite_loop(self):
        # Test to ensure that the function does not end in an infinite loop
        try:
            truckLoadPackages(self.truck, self.packages)
        except RuntimeError:
            self.fail("truckLoadPackages() resulted in an infinite loop.")

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
