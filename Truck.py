from datetime import timedelta
from CSV import *

class Truck:
    """
    Represents a delivery truck that can carry packages.

    Attributes:
        truckId (int): The unique ID for the truck.
        packages (list): A list of packages currently loaded onto the truck.
        currentLocation (str): The current location of the truck, starting at the hub.
        totalMileage (float): The total mileage driven by the truck.
        currentTime (timedelta): The current time for the truck's schedule, starting at 8:00 AM.
        hashTable (dict): A reference to the hash table for updating package statuses.
        capacity (int): The maximum number of packages the truck can carry.
    """
    def __init__(self, truckId, hashTable):
        """
        Initializes a Truck instance.

        Args:
            truckId (int): The unique ID for the truck.
            hashTable (dict): A reference to the hash table for managing package statuses.

        Attributes Initialized:
            truckId: Assigned based on the given parameter.
            packages: Initialized as an empty list for holding loaded packages.
            currentLocation: Initialized as "Hub" (the starting location).
            totalMileage: Set to 0.0 initially, representing the mileage driven by the truck.
            currentTime: Initialized to 8:00 AM using timedelta(hours=8).
            hashTable: Reference to the hash table passed as a parameter.
            capacity: Set to 16 packages.
        """
        self.truckId = truckId
        self.packages = []  # List of packages assigned to the truck
        self.currentLocation = "Hub" #TODO is this the address? 4001 South 700 East, Salt Lake City, UT 84107
        self.totalMileage = 0.0
        self.currentTime = timedelta(hours=8)  # Start at 8:00 AM
        self.hashTable = hashTable  # Reference to hash table for updating package status
        self.capacity = 16  # Each truck can carry a maximum of 16 packages

    # def loadPackage(self, package):
    #     """
    #     Loads a package onto the truck if capacity allows.
    #     :param package: Package object to load.
    #     """
    #     if package is None:
    #         print("Warning: Attempted to load a None package.")
    #         return
    #
    #     if len(self.packages) < self.capacity:
    #         self.packages.append(package)
    #         print(f"Package {package.packageID} loaded onto Truck {self.truckId}.")
    #     else:
    #         print(f"Truck {self.truckId} is at full capacity, cannot load Package {package.packageID}.")
    #
    # def deliverPackages(self):
    #     """
    #     Delivers all packages loaded on the truck based on the nearest neighbor algorithm,
    #     choosing the nearest address first.
    #     Updates the delivery status and total mileage.
    #     """
    #     while self.packages:
    #         # Find the closest package to the current address using the nearest neighbor algorithm
    #         closestPackage = minDistanceFrom(self.currentLocation, self.packages)
    #
    #         # Calculate the distance to the next package address
    #         distanceToNext = distanceBetween(self.currentLocation, closestPackage.deliveryAddress)
    #
    #         # Update the truck's mileage and move to the next address
    #         self.totalMileage += distanceToNext
    #         self.currentLocation = closestPackage.deliveryAddress
    #
    #         # Calculate time taken for the delivery based on the average speed of 18 mph
    #         timeToDeliver = timedelta(hours=distanceToNext / 18)
    #         self.currentTime += timeToDeliver
    #
    #         # Update the package delivery status and delivery time in the hash table
    #         closestPackage.updateStatus("Delivered", deliveryTime=self.currentTime)
    #         self.hashTable.insert(closestPackage.packageID, closestPackage)
    #
    #         # Print delivery information
    #         print(f"Package {closestPackage.packageID} delivered to {closestPackage.deliveryAddress} at {self.currentTime}. Truck {self.truckId} total mileage: {self.totalMileage:.2f} miles.")
    #
    #         # Remove the delivered package from the truck's package list
    #         self.packages.remove(closestPackage)

    def __str__(self):
        """
        TODO do we need this to string?????????
        Returns a string representation of the Truck object.

        Returns:
            str: A string representing the truck ID and the number of packages loaded.
        """
        return f"Truck {self.truckId} with {len(self.packages)} packages loaded."
