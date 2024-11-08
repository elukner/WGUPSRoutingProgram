import unittest
from Package import Package

class PackageTestCase(unittest.TestCase):

    def setUp(self):
        # Create a package instance for testing
        self.package = Package(
            packageID=1,
            deliveryAddress="195 W Oakland Ave",
            city="Salt Lake City",
            state="UT",
            zip="84115",
            deliveryDeadline="10:30 AM",
            packageWeight=21,
            pageSpecialNotes="Handle with care",
            deliveryStatus="At Hub"
        )

    def test__init__(self):
        self.assertEqual(True, False)  # add assertion here

    def testUpdateStatus(self):
        self.assertEqual(True, False)  # add assertion here

    def test__str__(self):
        self.assertEqual(True, False)  # add assertion here

    def test_str_method(self):
        # Test the string representation of the package
        expected_str = (
            "1, 195 W Oakland Ave, Salt Lake City, UT, 84115, 10:30 AM, 21, Handle with care, At Hub, Not Delivered")
        self.assertEqual(str(self.package), expected_str)
        #print(self.package) TODO delete later?


if __name__ == '__main__':
    unittest.main()
