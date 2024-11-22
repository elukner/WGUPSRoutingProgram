# This Python file contains supporting functions for the WGUPS Routing Program.
from Package import *
from HashTable import *
from Truck import *
from datetime import timedelta

# Global variables to store the data
distanceData = []
addressData = []


def loadDistanceData(fileName):
    """
    Reads distance data from the provided CSV file and appends each row to the distanceData list.

    Args:
        fileName (str): The name of the CSV file containing distance data.

    Returns:
        list: A 2D list containing distances between addresses.
    """
    global distanceData

    with open(fileName) as csvfile:
        distanceDataReader = csv.reader(csvfile, delimiter=',')

        # Read each row in the CSV file
        for row in distanceDataReader:
            cleanedRow = []
            for value in row:
                try:
                    # Convert value to float; if empty, set to 0.0
                    cleanedRow.append(float(value) if value else 0.0)
                except ValueError:
                    # If there's a problem converting, set value to 0.0
                    cleanedRow.append(0.0)

            # Append the cleaned row to distanceData
            distanceData.append(cleanedRow)

    return distanceData


def loadAddressData(fileName):
    """
    Reads address data from the provided CSV file and appends each address to the addressData list.
    """
    currentAddressData = addressData

    with open(fileName) as csvfile:
        addressDataReader = csv.reader(csvfile, delimiter=',')

        # Iterate over each row in the CSV file
        for row in addressDataReader:
            if len(row) > 2:
                # Extract the address from the third column (index 2)
                address = row[2].strip()
                if address:
                    #TODO delete later print(address)
                    currentAddressData.append(address)

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
    with open(fileName, encoding='utf-8-sig') as packageCSV:
        packageData = csv.reader(packageCSV, delimiter=',')

        # Iterate through each row in the CSV file
        for package in packageData:
            # Skip empty rows or rows with missing values
            if len(package) == 0 or package[0].strip() == '' or not package[0].isdigit():
                continue

            try:
                # Extract data from each column in the row
                packageID = int(package[0].strip())
                deliveryAddress = package[1].strip()
                city = package[2].strip()
                state = package[3].strip()
                zip = package[4].strip()
                deliveryDeadline = package[5].strip() if package[5] else "EOD"
                packageWeight = int(package[6].strip()) if package[6].strip().isdigit() else 0
                pageSpecialNotes = package[7].strip() if len(package) > 7 else ""
                deliveryStatus = "At Hub"  # Setting initial status to be "At Hub"

                # Calculate the distance from the hub to the package address if available
                hubAddress = "4001 South 700 East"  # Replace with actual Hub address
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
    # Start by filtering packages that are allowed to be loaded into the current truck
    available_packages = [pkg for pkg in packages if pkg.allowedTruck is None or pkg.allowedTruck == truck.truckId]

    # Load group-dependent packages first, to ensure they are delivered together
    group_packages = [pkg for pkg in available_packages if pkg.groupDependency]
    for pkg in group_packages:
        if len(truck.packages) < truck.capacity and pkg in available_packages:
            truck.loadPackage(pkg)
            packages.remove(pkg)
            available_packages.remove(pkg)

            # Also load dependent packages, if they exist and meet the conditions
            for dependent_id in pkg.groupDependency:
                dependent_pkg = next((p for p in available_packages if p.packageID == dependent_id), None)
                if dependent_pkg and len(truck.packages) < truck.capacity:
                    truck.loadPackage(dependent_pkg)
                    packages.remove(dependent_pkg)
                    available_packages.remove(dependent_pkg)

    #Load all the packages that have special notes for specific trucks
    for pkg in available_packages:
        if(pkg.allowedTruck == truck.truckId):
            truck.loadPackage(pkg)
            packages.remove(pkg)
            available_packages.remove(pkg)


    # Load remaining packages using nearest neighbor approach
    while len(truck.packages) < truck.capacity and available_packages:
        # Find the closest package from the current location
        closestPackage = minDistanceFrom(truck.currentLocation, available_packages)


        if closestPackage:
            if(closestPackage.arrivalTime is not None and (closestPackage.arrivalTime>truck.currentTime)):
                available_packages.remove(closestPackage)
                continue
            # Load the package onto the truck
            truck.loadPackage(closestPackage)
            packages.remove(closestPackage)
            available_packages.remove(closestPackage)
            # TODO delete later
            # print(f"Truck {truck.truckId} loaded package {closestPackage.packageID}.")
        else:
            print("No valid package found to load.")
            break

    # Finally, load delayed packages if their arrival time has passed
    for pkg in list(packages):
        if pkg.arrivalTime and truck.currentTime >= pkg.arrivalTime and len(truck.packages) < truck.capacity:
            truck.loadPackage(pkg)
            packages.remove(pkg)
            # TODO delete later
            # print(f"Truck {truck.truckId} loaded delayed package {pkg.packageID}.")


def deliverTruckPackages(truck,delayedPackages):
    """
    Delivers all packages loaded on the truck based on the nearest neighbor algorithm,
    choosing the nearest address first.
    Updates the delivery status and total mileage.
    """
    while truck.packages:
        # Find the closest package to the current address using the nearest neighbor algorithm
        #TODO delete later print(minDistanceFrom(truck.currentLocation, truck.packages))
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

        # Calculate time taken for the delivery based on the average speed of 18 mph TODO use the timeTo Deliver funciton
        timeToDeliver = timedelta(hours=distanceToNext / 18)
        truck.currentTime += timeToDeliver

        # Update the package delivery status and delivery time in the hash table
        closestPackage.updateStatus(f"Delivered by truck {truck.truckId}", deliveryTime=truck.currentTime)
        truck.hashTable.insert(closestPackage.packageID, closestPackage)

        # TODO delete later Print delivery information
        # print(
        #     f"Package {closestPackage.packageID} delivered to {closestPackage.deliveryAddress} at {truck.currentTime}. Truck {truck.truckId} total mileage: {truck.totalMileage:.2f} miles.")

        # Remove the delivered package from the truck's package list
        truck.packages.remove(closestPackage)

        # Check if any delayed packages are now available for pickup
        for pkg in delayedPackages:
            if pkg.arrivalTime and truck.currentTime >= pkg.arrivalTime:
                returnToHubAndLoadDelayedPackages(truck, delayedPackages)
                break  # Only go back once after finding at least one package that is ready


def returnToHubAndLoadDelayedPackages(truck, delayed_packages):
    """
    Returns the truck to the hub and loads the available delayed packages.
    :param truck: Truck object that needs to return to the hub.
    :param delayed_packages: List of delayed packages waiting at the hub.
    """
    # Assuming the hub is at "4001 South 700 East"
    hubAddress = "4001 South 700 East"
    distanceToHub = distanceBetween(truck.currentLocation, hubAddress)

    # Update truck mileage and current location
    truck.totalMileage += distanceToHub
    truck.currentLocation = hubAddress
    truck.currentTime += timedelta(hours=distanceToHub / 18)  # Assuming average speed of 18 mph

    # Load available delayed packages
    for pkg in list(delayed_packages):
        if pkg.arrivalTime and truck.currentTime >= pkg.arrivalTime:
            truck.loadPackage(pkg)
            delayed_packages.remove(pkg)
            # Optional: print for debugging
            # print(f"Truck {truck.truckId} loaded delayed package {pkg.packageID}.")


def deliverTruckPackagesUntil(truck, stopTime):
    """
    Delivers packages loaded on the truck until the specified stop time.
    Updates package delivery statuses and records total mileage.

    Args:
        truck (Truck): The truck object containing packages to be delivered.
        stopTime (timedelta): The time at which deliveries should stop.
    """
    while truck.packages:
        # Find the closest package to the current address using the nearest neighbor algorithm
        closestPackage = minDistanceFrom(truck.currentLocation, truck.packages)

        # Calculate the distance to the next package address
        distanceToNext = distanceBetween(truck.currentLocation, closestPackage.deliveryAddress)

        # Calculate time taken for the delivery based on the average speed of 18 mph
        timeToDeliver = timedelta(hours=distanceToNext / 18)

        # Check if the current time + time to deliver exceeds the stop time
        if truck.currentTime + timeToDeliver > stopTime:
            # If so, stop deliveries and break the loop
            break

        # Update the truck's mileage and move to the next address
        truck.totalMileage += distanceToNext
        truck.currentLocation = closestPackage.deliveryAddress
        truck.currentTime += timeToDeliver

        # Update the package delivery status and delivery time in the hash table
        closestPackage.updateStatus(f"Delivered by truck {truck.truckId}", deliveryTime=truck.currentTime)
        truck.hashTable.insert(closestPackage.packageID, closestPackage)

        # Print delivery information
        # print(
        #     f"Package {closestPackage.packageID} delivered to {closestPackage.deliveryAddress} at {truck.currentTime}. "
        #     f"Truck {truck.truckId} total mileage: {truck.totalMileage:.2f} miles.")

        # Remove the delivered package from the truck's package list
        truck.packages.remove(closestPackage)

    # For all remaining packages on the truck that haven't been delivered by the stopTime, update the status as 'En Route'
    for package in truck.packages:
        package.updateStatus("En Route")
        truck.hashTable.insert(package.packageID, package)

    # Print the status of all packages on the truck
    # print(f"\nStatus of packages on Truck {truck.truckId} as of {truck.currentTime}:")
    # for package in truck.packages:
    #     print(f"PackageID: {package.packageID}, Status: {package.deliveryStatus}, DeliveryTime: "
    #           f"{package.deliveryTime if package.deliveryTime else 'Not Delivered'}")


def distanceBetween(address1, address2):
    """
    Function to return the distance between two addresses.
    :param address1: The starting address.
    :param address2: The destination address.
    :return: Distance in miles between address1 and address2.
    """
    try:
        # print(f"Looking up: {address1} and {address2}")
        # print(f"Available addresses: {addressData}")
        index1 = addressData.index(address1)
        index2 = addressData.index(address2)
        distance=distanceData[index1][index2]
        if distance != 0:
            return distanceData[index1][index2]
        return distanceData[index2][index1]
    except ValueError as e:
        # If the address is not found, return a large value (inf) to indicate it is unreachable
        print(f"ValueError: Address not found - {e}")
        return float('inf')


# Function to find min distance/address
def minDistanceFrom(fromAddress, truckPackages) -> Package:
    """
    Function to find the package with the minimum distance from the given address.
    :param fromAddress: The address to calculate distances from.
    :param truckPackages: List of packages that need to be delivered.
    :return: The package object with the minimum distance to fromAddress.
    """
    # If truckPackages is empty, return None
    if not truckPackages:
        return None

    #TODO delete later? for dubugging purposes only
    #print(f"Finding the closest package to: {fromAddress}")

    # Find the closest package using the nearest neighbor approach
    closestPackage = min(
        truckPackages,
        key=lambda pkg: distanceBetween(fromAddress, pkg.deliveryAddress) if distanceBetween(fromAddress, pkg.deliveryAddress) != float('inf') else float('inf'),
        default=None
    )

    #TODO delete later? for dubugging purposes only
    # if closestPackage:
    #     print(f"Closest package to {fromAddress} is {closestPackage.packageID} at address {closestPackage.deliveryAddress}")
    # else:
    #     print(f"No valid closest package found from {fromAddress}")

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



