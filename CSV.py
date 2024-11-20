# This Python file contains supporting functions for the WGUPS Routing Program.
from Package import *
from HashTable import *
from Truck import *
from CSV import *
import csv
from datetime import timedelta

# Global variables to store the data
distanceData = []
addressData = []


def loadDistanceData(fileName):
    """
    Reads distance data from the provided CSV file and appends each row to the distanceData list.
    """
    currentDistanceData = distanceData

    with open(fileName) as csvfile:
        distanceDataReader = csv.reader(csvfile, delimiter=',')
        # Skip the first row
        for i in range(8):
            next(distanceDataReader)

        for row in distanceDataReader:
            cleanedRow = []
            for value in row[1:]:
                try:
                    cleanedRow.append(float(value))
                except ValueError:
                    cleanedRow.append(0.0)
            currentDistanceData.append(cleanedRow)
    return currentDistanceData


def loadAddressData(fileName):
    """
    Reads address data from the provided CSV file and appends each address to the addressData list.
    """
    currentAddressData = addressData

    with open(fileName) as csvfile:
        addressDataReader = csv.reader(csvfile, delimiter=',')
        # Skip the first row
        next(addressDataReader)
        for row in addressDataReader:
            if len(row) > 0:
                address = row[2].strip()  # Extract the address from the first column (index 0)
                if address:
                    addressData.append(address)
    return currentAddressData


def loadPackageData(fileName, hashTable):
    """
    This function reads package data from the provided CSV file, creates and updates
    Package objects for each entry, and inserts them into a hash table.

    Steps:
    1. Reads the package data from the packageCSV file.
    2. Updates each Package object with its respective data, including address, deadline, weight, etc.
    3. Inserts each Package object into the hash table using the package ID as the key.
    :param fileName: The name of the CSV file containing package data.
    :param hashTable: The hash table into which Package objects will be inserted, with the package ID as the key.
    """
    with open(fileName) as packageCSV:
        packageData = csv.reader(packageCSV, delimiter=',')

        # Skip the first row if it is a header
        next(packageData)

        for package in packageData:
            # Skip empty rows or rows with missing values
            if len(package) == 0 or package[0].strip() == '' or not package[0].isdigit():
                continue

            try:
                packageID = int(package[0].strip())
                deliveryAddress = package[1].strip()
                city = package[2].strip()
                state = package[3].strip()
                zip = package[4].strip()
                deliveryDeadline = package[5].strip()
                packageWeight = package[6].strip()
                pageSpecialNotes = package[7].strip() if len(package) > 7 else ""
                deliveryStatus = "At Hub"  # Setting initial status to be "At Hub"

                # Calculate the distance from the hub to the package address
                hubAddress = "Hub Address"  # Replace with actual Hub address
                try:
                    indexFrom = addressData.index(hubAddress)
                    indexTo = addressData.index(deliveryAddress)
                    distance = distanceData[indexFrom][indexTo]
                    deliveryTime = timeToDeliver(distance)
                except ValueError:
                    # If address is not found, set deliveryTime to None
                    deliveryTime = None

                # Create Package object
                package = Package(packageID, deliveryAddress, city, state, zip, deliveryDeadline,
                                  packageWeight, pageSpecialNotes, deliveryStatus, deliveryTime)

                # Insert it into the hash table
                hashTable.insert(packageID, package)

            except ValueError as e:
                print(f"Skipping invalid row in {fileName}: {package} ({e})")


def truckLoadPackages(truck, packages):
    """
    Loads packages into the truck using the nearest neighbor approach until the truck is full.
    :param truck: Truck object that packages need to be loaded into.
    :param packages: List of packages available for loading.
    """
    remaining_packages = packages.copy()
    while len(truck.packages) < truck.capacity and remaining_packages:
        # Find the closest package from the current location
        closest_package = minDistanceFrom(truck.currentLocation, remaining_packages)

        # Break the loop if no valid package is found
        if closest_package is None:
            print("Warning: No valid package found to load.")
            break

        # Load the package onto the truck
        truck.loadPackage(closest_package)

        # Remove the loaded package from the remaining_packages list
        remaining_packages = [
            package for package in remaining_packages if package.packageID != closest_package.packageID
        ]

        # If the truck reaches capacity, break the loop
        if len(truck.packages) >= truck.capacity:
            break
    # TODO el: the packages get removed from remaining_packages but don't get removed from the global
    #  packages variable.
    #  So then all the packages get sent to the next truck instead of just the ones that are left.


def distanceBetween(address1, address2):
    """
    Function to return the distance between two addresses.
    :param address1: The starting address.
    :param address2: The destination address.
    :return: Distance in miles between address1 and address2.
    """
    try:
        return distanceData[addressData.index(address1)][addressData.index(address2)]
    except ValueError:
        # If the address is not found, return a large value (inf) to indicate it is unreachable
        return float('inf')


# Function to find min distance/address
def minDistanceFrom(fromAddress, truckPackages):
    """
    Function to find the package with the minimum distance from the given address.
    :param fromAddress: The address to calculate distances from.
    :param truckPackages: List of packages that need to be delivered.
    :return: The package object with the minimum distance to fromAddress.
    """
    # If truckPackages is empty, return None
    if not truckPackages:
        return None

    minDistance = float("inf")
    closestPackage = None

    # Loop through all packages in the truck to find the closest package
    for truckPackage in truckPackages:
        distance = distanceBetween(fromAddress, truckPackage.deliveryAddress)

        # Skip the distance if it is 'inf', meaning the address is unreachable
        if distance == float('inf'):
            continue

        if distance < minDistance:
            minDistance = distance
            closestPackage = truckPackage

    return closestPackage

def deliverTruckPackages(truck):
    """
    Delivers all packages loaded on the truck based on the nearest neighbor algorithm,
    choosing the nearest address first.
    Updates the delivery status and total mileage.
    """
    startingAddress="4001 South 700 East"
    while truck.packages:
        # Find the closest package to the current address using the nearest neighbor algorithm
        #closestPackage = minDistanceFrom(truck.currentLocation, truck.packages)
        closestPackage = minDistanceFrom(startingAddress, truck.packages)

        # Calculate the distance to the next package address
        #distanceToNext = distanceBetween(truck.currentLocation, closestPackage.deliveryAddress) not doing this in here
        #

        # Update the truck's mileage and move to the next address
        truck.totalMileage += distanceToNext
        truck.currentLocation = closestPackage.deliveryAddress

        # Calculate time taken for the delivery based on the average speed of 18 mph
        timeToDeliver = timedelta(hours=distanceToNext / 18)
        truck.currentTime += timeToDeliver

        # Update the package delivery status and delivery time in the hash table
        closestPackage.updateStatus("Delivered", deliveryTime=truck.currentTime)
        truck.hashTable.insert(closestPackage.packageID, closestPackage)

        # Print delivery information
        print(f"Package {closestPackage.packageID} delivered to {closestPackage.deliveryAddress} at {truck.currentTime}. Truck {truck.truckId} total mileage: {truck.totalMileage:.2f} miles.")

        # Remove the delivered package from the truck's package list
        truck.packages.remove(closestPackage)

# Function to calculate time to deliver
def timeToDeliver(distance):
    """
    Function to calculate the time required to deliver based on distance.
    Assumes an average speed of 18 mph.
    :param distance: Distance that will be traveled in miles.
    :return: Time in hours required to travel the given distance.
    """
    averageSpeedMph = 18  # Assumption that trucks travel at an average speed of 18 miles per hour
    return distance / averageSpeedMph
