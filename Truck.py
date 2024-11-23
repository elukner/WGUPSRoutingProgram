from datetime import timedelta
from CSV import *


class Truck:
    """
    Class Truck represents a delivery truck that can carry packages.
    """

    def __init__(self, truckId, hashTable):
        """
        Initializes a Truck instance.
        :param truckId: The unique ID for the truck.
        :param hashTable: A reference to the hash table for managing package statuses.
        """
        self.truckId = truckId  # Assigned based on the given parameter.
        self.packages = []  # Initialized as an empty list for holding loaded packages.
        self.currentLocation = "4001 South 700 East"  # The starting location which is the Hub address.
        self.totalMileage = 0.0  # Set to 0.0 initially, representing the mileage driven by the truck.
        self.currentTime = timedelta(hours=8)  # Start at 8:00 AM
        self.hashTable = hashTable  # Reference to hash table for updating package status
        self.capacity = 16  # Each truck can carry a maximum of 16 packages

    def __str__(self):
        """
        Returns a string representation of the Truck object.
        :return: str: A string representing the truck ID and the number of packages loaded.
        """
        return f"Truck {self.truckId} with {len(self.packages)} packages loaded."

    def loadPackage(self, package):
        """
        Loads a package onto the truck if capacity allows.
        :param package: The package object to be loaded onto the truck.
        :return: bool: True if the package was successfully loaded, False if the truck is at full capacity.
        """
        if len(self.packages) < self.capacity:
            self.packages.append(package)
            package.updateStatus("In Route", deliveryTime=self.currentTime)
            return True
        else:
            return False
