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

    def testInitialStatus(self):
        # Verify the initial status of the package is "At Hub"
        self.assertEqual(self.package.deliveryStatus, "At Hub")
        # Verify the delivery time is None initially
        self.assertIsNone(self.package.deliveryTime)

    def testUpdateStatusEnRoute(self):
        # Update the status to "En Route"
        self.package.updateStatus("En Route")
        # Verify that the status is updated correctly
        self.assertEqual(self.package.deliveryStatus, "En Route")
        # Verify that delivery time remains None
        self.assertIsNone(self.package.deliveryTime)

    def testUpdateStatusDelivered(self):
        # Update the status to "Delivered" with a delivery time
        delivery_time = "12:45 PM"
        self.package.updateStatus("Delivered", deliveryTime=delivery_time)
        # Verify that the status is updated to "Delivered"
        self.assertEqual(self.package.deliveryStatus, "Delivered")
        # Verify that the delivery time is updated
        self.assertEqual(self.package.deliveryTime, delivery_time)

    def testUpdateStatusDeliveredWithoutTime(self):
        # Update the status to "Delivered" without specifying the delivery time
        self.package.updateStatus("Delivered")
        # Verify that the status is updated to "Delivered"
        self.assertEqual(self.package.deliveryStatus, "Delivered")
        # Verify that the delivery time is still None (as it was not specified)
        self.assertIsNone(self.package.deliveryTime)

    def test__str__(self):
        # Test the string representation of the package
        expected_str = (
            "1, 195 W Oakland Ave, Salt Lake City, UT, 84115, 10:30 AM, 21, Handle with care, At Hub, Not Delivered")
        self.assertEqual(str(self.package), expected_str)
        #print(self.package) TODO delete later?


if __name__ == '__main__':
    unittest.main()
