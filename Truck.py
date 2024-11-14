from datetime import timedelta
from CSV import *

class Truck:
    def __init__(self, truckId, hashTable):
        self.truckId = truckId
        self.packages = []  # List of packages assigned to the truck
        self.currentLocation = "Hub" #TODO is this the address? 4001 South 700 East, Salt Lake City, UT 84107
        self.totalMileage = 0.0
        self.currentTime = timedelta(hours=8)  # Start at 8:00 AM
        self.hashTable = hashTable  # Reference to hash table for updating package status
        self.capacity = 16  # Each truck can carry a maximum of 16 packages

    def loadPackage(self, package):
        """
        Loads a package onto the truck if capacity allows.
        :param package: Package object to load.
        """
        if len(self.packages) < self.capacity:
            self.packages.append(package)
            print(f"Package {package.packageID} loaded onto Truck {self.truckId}.")
        else:
            print(f"Truck {self.truckId} is at full capacity, cannot load Package {package.packageID}.")

    def deliverPackages(self):
        """
        Delivers all packages loaded on the truck based on the nearest neighbor algorithm,
        choosing the nearest address first.
        Updates the delivery status and total mileage.
        """
        while self.packages:
            # Find the closest package to the current address using the nearest neighbor algorithm
            closestPackage = minDistanceFrom(self.currentLocation, self.packages)

            # Calculate the distance to the next package address
            distanceToNext = distanceBetween(self.currentLocation, closestPackage.deliveryAddress)

            # Update the truck's mileage and move to the next address
            self.totalMileage += distanceToNext
            self.currentLocation = closestPackage.deliveryAddress

            # Calculate time taken for the delivery based on the average speed of 18 mph
            timeToDeliver = timedelta(hours=distanceToNext / 18)
            self.currentTime += timeToDeliver

            # Update the package delivery status and delivery time in the hash table
            closestPackage.updateStatus("Delivered", deliveryTime=self.currentTime)
            self.hashTable.insert(closestPackage.packageID, closestPackage)

            # Print delivery information
            print(f"Package {closestPackage.packageID} delivered to {closestPackage.deliveryAddress} at {self.currentTime}. Truck {self.truckId} total mileage: {self.totalMileage:.2f} miles.")

            # Remove the delivered package from the truck's package list
            self.packages.remove(closestPackage)

    def __str__(self):
        return f"Truck {self.truckId} with {len(self.packages)} packages loaded."
