import unittest
from datetime import timedelta
from Truck import Truck
from Package import Package



class TruckTestCase(unittest.TestCase):
    def setUp(self):
        # Create a mock hash table (could be an empty dictionary)
        self.hashTable = {}

        # Create a Truck instance
        self.truck = Truck(truckId=1, hashTable=self.hashTable)

    def test_initialization(self):
        # Test if the truck is initialized with correct values
        self.assertEqual(self.truck.truckId, 1)
        self.assertEqual(len(self.truck.packages), 0)
        self.assertEqual(self.truck.currentLocation, "Hub")
        self.assertEqual(self.truck.totalMileage, 0.0)
        self.assertEqual(self.truck.currentTime, timedelta(hours=8))
        self.assertEqual(self.truck.capacity, 16)

    # def test_str_representation(self):
    #     # Test the string representation of the truck
    #     self.assertEqual(str(self.truck), "Truck 1 with 0 packages loaded.")
    #
    #     # Load a package and check again
    #     package1 = Package(1, "195 W Oakland Ave", "Salt Lake City", "UT", "84115", "10:30 AM", 21, "")
    #     self.truck.loadPackage(package1)
    #     self.assertEqual(str(self.truck), "Truck 1 with 1 packages loaded.")

if __name__ == '__main__':
    unittest.main()
