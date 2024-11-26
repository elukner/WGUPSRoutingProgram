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
    :param fileName: The name of the CSV file containing distance data.
    :return: list: A 2D list containing distances between addresses.
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

    :param fileName: The name of the CSV file containing address data.
    :return: List of addresses read from the CSV file.
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
                    currentAddressData.append(address)

    return currentAddressData


def loadPackageData(fileName, hashTable):
    """
    This function reads package data from the provided CSV file, creates and updates
    Package objects for each entry, and inserts them into a hash table.
    :param fileName: The name of the CSV file containing package data.
    :param hashTable: The hash table into which Package objects will be inserted, with the package ID as the key.
    :return: None
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
                hubAddress = "4001 South 700 East"
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
    :return: None
    """
    # Load group-dependent packages first, to ensure they are delivered together
    groupPackagesList = [pkg for pkg in packages if pkg.groupDependency]

    # Then, load the rest of the edge cases specific to that package
    specificTruckList = [pkg for pkg in packages if pkg.allowedTruck == truck.truckId]
    delayedList = [pkg for pkg in packages if pkg.arrivalTime and pkg.arrivalTime <= truck.currentTime]
    wrongAddressList = [pkg for pkg in packages if pkg.addressCorrectionNeeded]

    # Load trucks with packages that must be delivered together
    for package in groupPackagesList:
        if len(truck.packages) < truck.capacity:
            truck.loadPackage(package)
            packages.remove(package)
            # if package.packageID == 9:
            #     print(f"Package 9 selected in groupPackagesList and loaded onto Truck {truck.truckId}.")
            # Load all dependent packages for this package
            for dependentId in package.groupDependency:
                # Find the actual dependent package in the list
                dependentPackage = next((p for p in packages if p.packageID == dependentId), None)
                if dependentPackage and len(truck.packages) < truck.capacity:
                    truck.loadPackage(dependentPackage)
                    packages.remove(dependentPackage)
                    # if package.packageID == 9:
                    #     print(f"Package 9 selected in groupPackagesList and loaded onto Truck {truck.truckId}.")

    # Load trucks with packages that have truck restriction
    for package in specificTruckList:
        if len(truck.packages) < truck.capacity:
            truck.loadPackage(package)
            packages.remove(package)
            # if package.packageID == 9:
            #     print(f"Package 9 selected in specificTruckList and loaded onto Truck {truck.truckId}.")


    # Load delayed packages if their arrival time has passed
    # for package in delayedList:
    #     if len(truck.packages) < truck.capacity:
    #         truck.loadPackage(package)
    #         packages.remove(package)
            # if package.packageID == 9:
            #     print(f"Package 9 selected in delayedList and loaded onto Truck {truck.truckId}.")


    # Load packages with wrong addresses during initial loading
    for package in wrongAddressList:
        if len(truck.packages) < truck.capacity:
            truck.loadPackage(package)
            packages.remove(package)
            if package.packageID == 9:
                print(f"Package 9 selected in wrongAddressList and loaded onto Truck {truck.truckId}.")

    # Load remaining packages using nearest neighbor approach
    availablePackages = [pkg for pkg in packages if pkg not in groupPackagesList
                         and pkg not in specificTruckList and pkg not in delayedList
                         and pkg not in wrongAddressList]

    while len(truck.packages) < truck.capacity and availablePackages:
        # Find the closest package from the current location
        # if len(truck.packages)>0:
        #     closestPackage = minDistanceFrom(truck.packages[0], availablePackages)
        # else:
        #     closestPackage = minDistanceFrom(truck.currentLocation, availablePackages)
        closestPackage = minDistanceFrom(truck.currentLocation, availablePackages)

        if closestPackage:
            # Ensure that the package's arrival time allows it to be loaded
            if closestPackage.arrivalTime and closestPackage.arrivalTime > truck.currentTime:
                availablePackages.remove(closestPackage)
                continue

            # Load the package onto the truck
            truck.loadPackage(closestPackage)
            packages.remove(closestPackage)
            availablePackages.remove(closestPackage)
        else:
            print("No valid package found to load.")
            break


def deliverTruckPackages(truck,stopTime):
    """
    Delivers all packages loaded on the truck based on the nearest neighbor algorithm,
    choosing the nearest address first and prioritizing packages with deadlines.
    Updates the delivery status and total mileage.

    :param truck: The Truck object that contains loaded packages to be delivered.
    :return: None
    """
    # Initialize correctPackage9 to track whether package #9 has been corrected
    correctPackage9 = False

    # Get packages that are currently available for delivery
    availablePackages = [pkg for pkg in truck.packages if (not pkg.arrivalTime or pkg.arrivalTime <= truck.currentTime) and not pkg.addressCorrectionNeeded]
    packagesWithDeadlines = [pkg for pkg in availablePackages if pkg.deliveryDeadline != 'EOD']

    while availablePackages:
        # Stop deliveries if current time exceeds the stop time
        if truck.currentTime >= stopTime:
            #TODO delete later print(f"Stopping deliveries at {truck.currentTime} due to stopTime limitation.")
            break

        # # Correct the address for package #9 after 10:20 AM
        # if truck.currentTime >= timedelta(hours=10, minutes=20):
        #     correctPackage9 = correctPackage9Address(truck)  # Corrects package #9's address in the hash table
        #correctPackage9Address(truck)  # Corrects package #9's address in the hash table
        # Correct the address for package #9 after 10:20 AM
        if (truck.currentTime >= timedelta(hours=10, minutes=20) and correctPackage9==False):
            correctPackage9 = True
            correctAddressAt1020(truck.hashTable)  # Corrects package #9's address in the hash table
            #truck.loadPackage(truck.hashTable.lookUp(9))
            print(f"Package #9 has has a address correction.")

        # Prioritize packages with deadlines if available, else use the nearest neighbor approach
        if packagesWithDeadlines:
            closestPackage = getClosestPackage(truck,packagesWithDeadlines)
            packagesWithDeadlines.remove(closestPackage)
        else:
            closestPackage = getClosestPackage(truck,availablePackages)


        # If no valid package is found, break the loop
        if closestPackage is None:
            print("Warning: No valid package found to deliver.")
            break

        # Calculate the distance to the next package address
        distanceToNext = distanceBetween(truck.currentLocation, closestPackage.deliveryAddress)
        if distanceToNext == float('inf'):
            print(f"Warning: Cannot deliver to {closestPackage.deliveryAddress}, unreachable.")
            availablePackages.remove(closestPackage)
            continue

        # Calculate the time taken to deliver based on the average speed of 18 mph
        timeToDeliver = timedelta(hours=distanceToNext / 18)

        # Check if the current time plus the time to deliver exceeds the stop time
        if truck.currentTime + timeToDeliver > stopTime:
           #TODO delete later print(f"Cannot deliver package {closestPackage.packageID} as it would exceed the stop time of {stopTime}.")
            break

        # Update the truck's mileage, location, and time
        updateTruckState(closestPackage, distanceToNext, truck)


        # if closestPackage.packageID==9:
        #     print(f"Closet package is delivered {closestPackage}")

        # Update the package delivery status and delivery time in the hash table
        closestPackage.updateStatus(f"Delivered by truck {truck.truckId}", deliveryTime=truck.currentTime)
        truck.hashTable.insert(closestPackage.packageID, closestPackage)


        # Remove the delivered package from truck's available packages
        truck.packages.remove(closestPackage)
        availablePackages.remove(closestPackage)


        # Reevaluate available packages to ensure delayed packages with deadlines are delivered on time
        availablePackages = [pkg for pkg in truck.packages if
                             (not pkg.arrivalTime or pkg.arrivalTime <= truck.currentTime) and not pkg.addressCorrectionNeeded]
        packagesWithDeadlines = [pkg for pkg in availablePackages if pkg.deliveryDeadline != 'EOD']


def updateTruckState(closestPackage, distanceToNext, truck):
    # Update the truck's mileage, location, and time
    truck.totalMileage += distanceToNext
    truck.currentLocation = closestPackage.deliveryAddress
    truck.currentTime += timedelta(hours=distanceToNext / 18)  # Assuming average speed is 18 mph


def getClosestPackage(truck, packages):
    # Prioritize packages with deadlines if available, else use the nearest neighbor approach
    return min(packages,
               key=lambda pkg: distanceBetween(truck.currentLocation, pkg.deliveryAddress))


def correctPackage9Address(truck):
    # Correct the address for package #9 after 10:20 AM
    if truck.currentTime >= timedelta(hours=10, minutes=20):
        correctAddressAt1020(truck.hashTable)  # Corrects package #9's address in the hash table
        print(f"Package #9 loaded onto Truck {truck.truckId} after address correction.")
        # package9 = truck.hashTable.lookUp(9)
        # if package9 not in truck.packages and len(truck.packages) < truck.capacity:
        #     truck.loadPackage(package9)
        #     print(f"Package #9 loaded onto Truck {truck.truckId} after address correction.")
           # return True

            #truck.packages.remove(package9)
        # Only load if package is not already on the truck and not delivered
        # if package9 not in truck.packages and not package9.deliveryStatus == "Delivered" and len(
        #         truck.packages) < truck.capacity:
        #     truck.loadPackage(package9)


def correctAddressAt1020(hashTable):
    """
    Corrects the address for package #9 at 10:20 AM.

    :param hashTable: The hash table containing package information.
    :return: None
    """
    package9 = hashTable.lookUp(9)
    if package9 and package9.addressCorrectionNeeded:
        package9.deliveryAddress = "410 S State St"
        package9.city = "Salt Lake City"
        package9.state = "UT"
        package9.zip = "84111"
        package9.addressCorrectionNeeded = False



def returnToHubAndLoadDelayedPackages(truck, delayedPackages):
    """
    Returns the truck to the hub and loads the available delayed packages.

    :param truck: Truck object that needs to return to the hub.
    :param delayedPackages: List of delayed packages waiting at the hub.
    :return: None
    """
    # The hub is address is "4001 South 700 East"
    hubAddress = "4001 South 700 East"
    distanceToHub = distanceBetween(truck.currentLocation, hubAddress)

    # Update truck mileage and current location
    truck.totalMileage += distanceToHub
    truck.currentLocation = hubAddress
    truck.currentTime += timedelta(hours=distanceToHub / 18)  # Assuming average speed of 18 mph

    # Load available delayed packages
    for pkg in list(delayedPackages):
        if truck.currentTime >= pkg.arrivalTime:
            truck.loadPackage(pkg)
            delayedPackages.remove(pkg)


def deliverTruckPackagesUntil(truck, stopTime):
    """
    Delivers packages loaded on the truck until the specified stop time.
    Updates package delivery statuses and records total mileage.
    :param truck: The truck object containing packages to be delivered.
    :param stopTime: The time at which deliveries should stop.
    :return: None
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

        # Remove the delivered package from the truck's package list
        truck.packages.remove(closestPackage)

    # For all remaining packages on the truck that haven't been delivered by the stopTime, update the status as 'En Route'
    for package in truck.packages:
        package.updateStatus("En Route")
        truck.hashTable.insert(package.packageID, package)


def distanceBetween(address1, address2):
    """
    Function to return the distance between two addresses.
    :param address1: The starting address.
    :param address2: The destination address.
    :return: Distance in miles between address1 and address2.
    """
    try:
        index1 = addressData.index(address1)
        index2 = addressData.index(address2)
        distance = distanceData[index1][index2]
        if distance != 0:
            return distanceData[index1][index2]
        return distanceData[index2][index1]
    except ValueError as e:
        # If the address is not found, return a large value (inf) to indicate it is unreachable
        print(f"ValueError: Address not found - {e}")
        return float('inf')


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

    # Find the closest package using the nearest neighbor approach
    closestPackage = min(
        truckPackages,
        key=lambda pkg: distanceBetween(fromAddress, pkg.deliveryAddress) if distanceBetween(fromAddress,
                                                                                             pkg.deliveryAddress) != float(
            'inf') else float('inf'),
        default=None
    )

    return closestPackage


def timeToDeliver(distance):
    """
    Function to calculate the time required to deliver based on distance.
    Assumes an average speed of 18 mph.
    :param distance: Distance that will be traveled in miles.
    :return: Time in hours required to travel the given distance.
    """
    averageSpeedMph = 18
    return distance / averageSpeedMph
