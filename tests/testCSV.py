import unittest
from CSV import *

# Mock Data for Testing
addressData = [
    "Hub Address",
    "195 W Oakland Ave",
    "2530 S 500 E",
    "233 Canyon Rd"
]

distanceData = [
    [0, 2.5, 3.0, 4.5],  # Distances from "Hub Address"
    [2.5, 0, 1.0, 2.0],  # Distances from "195 W Oakland Ave"
    [3.0, 1.0, 0, 3.5],  # Distances from "2530 S 500 E"
    [4.5, 2.0, 3.5, 0]   # Distances from "233 Canyon Rd"
]


class CSVTestCase(unittest.TestCase):
    def test_valid_addresses(self):
        # Test a valid case where both addresses exist
        distance = distanceBetween("Hub Address", "195 W Oakland Ave")
        self.assertEqual(distance, 2.5, "Distance between 'Hub Address' and '195 W Oakland Ave' should be 2.5 miles")

        distance = distanceBetween("195 W Oakland Ave", "2530 S 500 E")
        self.assertEqual(distance, 1.0, "Distance between '195 W Oakland Ave' and '2530 S 500 E' should be 1.0 mile")

    def test_same_address(self):
        # Test when the starting and ending address are the same
        distance = distanceBetween("Hub Address", "Hub Address")
        self.assertEqual(distance, 0, "Distance between the same address should be 0")

    def test_address_not_found(self):
        # Test when one or both addresses are not in the addressData list
        distance = distanceBetween("Non-existent Address", "195 W Oakland Ave")
        self.assertEqual(distance, float('inf'), "Distance should be inf for an unknown address")

        distance = distanceBetween("Hub Address", "Unknown Address")
        self.assertEqual(distance, float('inf'), "Distance should be inf for an unknown address")

    def test_both_addresses_not_found(self):
        # Test when both addresses are not in the addressData list
        distance = distanceBetween("Unknown Address A", "Unknown Address B")
        self.assertEqual(distance, float('inf'), "Distance should be inf when both addresses are unknown")


    #def testMinDistanceFrom(self):
     #   self.assertEqual(True, False)  # add assertion here

    #def testTimeToDeliver(self):
    #    self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()
