import unittest
from datetime import timedelta
from io import StringIO
from CSV import distanceBetween, minDistanceFrom, timeToDeliver
from Package import Package

# Mock global data for distance and address information
global distanceData, addressData
distanceData = [
    [0, 5.0, 10.0, 7.5],  # Distances from Hub
    [5.0, 0, 4.0, 8.0],    # Distances from Address A
    [10.0, 4.0, 0, 3.0],   # Distances from Address B
    [7.5, 8.0, 3.0, 0]     # Distances from Address C
]
addressData = [
    "4001 South 700 East",  # Hub Address
    "195 W Oakland Ave",    # Address A
    "2530 S 500 E",         # Address B
    "233 Canyon Rd"         # Address C
]


class CSVTestCase(unittest.TestCase):
    def test_distanceBetween(self):
        # Test a valid distance lookup
        self.assertEqual(distanceBetween('1330 2100 S', '1060 Dalton Ave S'), 7.1)
        self.assertEqual(distanceBetween("195 W Oakland Ave", "2530 S 500 E"), 4.0)

        # Test distance lookup for same address (should be 0)
        self.assertEqual(distanceBetween("195 W Oakland Ave", "195 W Oakland Ave"), 0)

        # # Test a case where one of the addresses does not exist
        # self.assertEqual(distanceBetween("Unknown Address", "195 W Oakland Ave"), float('inf'))
        # self.assertEqual(distanceBetween("195 W Oakland Ave", "Unknown Address"), float('inf'))

    def test_minDistanceFrom(self):
        # Create mock packages with different addresses
        package1 = Package(1, "195 W Oakland Ave", "Salt Lake City", "UT", "84115", "10:30 AM", 21, "")
        package2 = Package(2, "2530 S 500 E", "Salt Lake City", "UT", "84106", "EOD", 44, "")
        package3 = Package(3, "233 Canyon Rd", "Salt Lake City", "UT", "84103", "EOD", 2, "")

        truckPackages = [package1, package2, package3]

        # Test finding the closest package from "4001 South 700 East" (Hub)
        closest_package = minDistanceFrom("4001 South 700 East", truckPackages)
        self.assertEqual(closest_package.packageID, 1)  # Package 1 is the closest (distance = 5.0)

        # Test finding the closest package from "195 W Oakland Ave"
        closest_package = minDistanceFrom("195 W Oakland Ave", truckPackages)
        self.assertEqual(closest_package.packageID, 2)  # Package 2 is the closest (distance = 4.0)

        # Test finding the closest package when all addresses are unreachable
        closest_package = minDistanceFrom("Unknown Address", truckPackages)
        self.assertIsNone(closest_package)  # No reachable packages

        # Test when there are no packages
        closest_package = minDistanceFrom("4001 South 700 East", [])
        self.assertIsNone(closest_package)  # Should return None when there are no packages

    def test_timeToDeliver(self):
        # Test time to deliver for various distances
        self.assertAlmostEqual(timeToDeliver(36), 2.0)  # 36 miles should take 2 hours at 18 mph
        self.assertAlmostEqual(timeToDeliver(9), 0.5)  # 9 miles should take 0.5 hours (30 minutes)
        self.assertAlmostEqual(timeToDeliver(0), 0.0)  # 0 miles should take 0 hours

        # Test time to deliver for a negative distance (should still return a value but may need input validation in real use)
        self.assertAlmostEqual(timeToDeliver(-18), -1.0)  # Negative values should be checked in real usage


if __name__ == '__main__':
    unittest.main()
