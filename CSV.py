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
    Loads packages into the truck based on the following rules:
    1. Some packages are assigned to specific trucks.
    2. Packages that need to be grouped together are loaded into the same truck.
    3. The nearest neighbor approach is used to load the remaining packages until the truck is full.

    Args:
        truck (Truck): Truck object that packages need to be loaded into.
        packages (list): List of Package objects available for loading.
    """
    # Define specific package assignments based on the requirements
    truck_assignments = {
        1: [1, 2, 3],  # Example: Truck 1 must have packages 1, 2, and 3
        2: [4, 5, 6],  # Example: Truck 2 must have packages 4, 5, and 6
        3: [7, 8, 9],  # Example: Truck 3 must have packages 7, 8, and 9
    }

    # Step 1: Load specific packages into the truck based on assignments
    if truck.truckId in truck_assignments:
        assigned_packages = [pkg for pkg in packages if pkg.packageID in truck_assignments[truck.truckId]]
        for package in assigned_packages:
            if len(truck.packages) < truck.capacity:
                truck.loadPackage(package)
                packages.remove(package)

    # Step 2: Use nearest neighbor approach to load the remaining packages
    while len(truck.packages) < truck.capacity and packages:
        # Find the closest package from the current location
        closest_package = minDistanceFrom(truck.currentLocation, packages)

        # Break the loop if no valid package is found
        if closest_package is None:
            print("Warning: No valid package found to load.")
            break

        # Load the package onto the truck
        truck.loadPackage(closest_package)

        # Remove the loaded package from the original packages list
        packages.remove(closest_package)

        # If the truck reaches capacity, break the loop
        if len(truck.packages) >= truck.capacity:
            break


def deliverTruckPackages(truck):
    """
    Delivers all packages loaded on the truck based on the nearest neighbor algorithm,
    choosing the nearest address first.
    Updates the delivery status and total mileage.
    """
    while truck.packages:
        # Find the closest package to the current address using the nearest neighbor algorithm
        print(minDistanceFrom(truck.currentLocation, truck.packages))
        closestPackage = minDistanceFrom(truck.currentLocation, truck.packages)

        # If no valid package is found, break the loop
        if closestPackage is None:
            print("Warning: No valid package found to deliver.")
            break

        # Calculate the distance to the next package address
        distanceToNext = distanceBetween(truck.currentLocation, closestPackage.deliveryAddress)
        if distanceToNext == float('inf'):
            print(f"Warning: Cannot deliver to {closestPackage.deliveryAddress}, unreachable.")
            break

        # Update the truck's mileage and move to the next address
        truck.totalMileage += distanceToNext
        truck.currentLocation = closestPackage.deliveryAddress

        # Calculate time taken for the delivery based on the average speed of 18 mph
        time_to_deliver = timedelta(hours=distanceToNext / 18)
        truck.currentTime += time_to_deliver

        # Update the package delivery status and delivery time in the hash table
        closestPackage.updateStatus("Delivered", deliveryTime=truck.currentTime)
        truck.hashTable.insert(closestPackage.packageID, closestPackage)

        # Print delivery information
        print(
            f"Package {closestPackage.packageID} delivered to {closestPackage.deliveryAddress} at {truck.currentTime}. Truck {truck.truckId} total mileage: {truck.totalMileage:.2f} miles.")

        # Remove the delivered package from the truck's package list
        truck.packages.remove(closestPackage)


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
