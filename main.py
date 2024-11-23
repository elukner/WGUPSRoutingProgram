# Student ID: 12345678  #TODO Replace with your actual student ID; this line identifies the submission.

from Package import *
from HashTable import *
from Truck import *
from CSV import *
import csv
from datetime import timedelta


def printUI():
    """
    Displays the main menu options for the user.
    """
    print(f'***************************************')
    print(f'1. Print All Package Status and Total Mileage')
    print(f'2. Get a Single Package Status with a Time')
    print(f'3. Get All Package Status with a Time')
    print(f'4. Exit the Program')
    print(f'***************************************')


def createPackageData():
    # Create the hash table and load package data
    hashTable = HashTable()
    loadPackageData('packageCSV.csv', hashTable)
    # check to see if hashtable data is all there TODO delete later
    # for packageIndex in range(1, 41):
    #    print(hashTable.lookUp(packageIndex))

    # Load data from CSV files
    loadDistanceData('distanceCSV.csv')
   #todo delete later
   # print(distanceData)
    loadAddressData('addressCSV.csv')
    #todo delete later
    #print(addressData)
    return hashTable


def initializeTrucks(numTrucks, hashTable):
    """
    Function to create and initialize a list of trucks.

    Args:
        num_trucks (int): The number of trucks to be created.
        hashTable (HashTable): Reference to the hash table for package status management.

    Returns:
        list: A list of initialized Truck objects.
    """
    trucks = []

    # Create trucks based on the number specified
    for i in range(1, numTrucks + 1):
        truck = Truck(truckId=i, hashTable=hashTable)
        trucks.append(truck)

    # # Print initial state of the trucks for verification
    # for truck in trucks:
    #     print(f"Truck ID: {truck.truckId}, "
    #           f"Current Location: {truck.currentLocation}, "
    #           f"Total Mileage: {truck.totalMileage}, "
    #           f"Packages Loaded: {len(truck.packages)}, "
    #           f"Capacity: {truck.capacity}, "
    #           f"Current Time: {truck.currentTime}")

    return trucks


def loadPackagesIntoTrucks(hashTable, truckList, totalPackages=40):
    """
    Function to load packages into trucks using the nearest neighbor approach.

    Args:
        hashTable (HashTable): Hash table containing all package information.
        truckList (list): A list of Truck objects to load packages into.
        totalPackages (int): Total number of packages to be loaded. Default is 40.

    Returns:
        list: Updated list of Truck objects with loaded packages.
    """
    # Get all packages from the hash table based on the package IDs
    packages = [hashTable.lookUp(packageID) for packageID in range(1, totalPackages + 1)]

    # Load packages into each truck
    for truck in truckList:
        truckLoadPackages(truck, packages)

    # TODO delete later Check to see if packages are loaded into trucks (for debugging purposes)
    # for truck in truckList:
    #     print('Truck ID:', truck.truckId, 'Packages:')
    #     for package in truck.packages:
    #         print(package)
    #         print()
    # TODO el packages are not loading into trucks

    return truckList

def deliverPackages(truckList):
    """
    Function to deliver packages for all trucks in the provided list.

    Args:
        truckList (list): A list of Truck objects that need to deliver their loaded packages.
    Notes:
        - This function assumes that all trucks in `truckList` have already been loaded with packages.
        - Each truck's status (including mileage, time, and package status) will be updated during the delivery process.
    """
    for truck in truckList:
        deliverTruckPackages(truck)



# def deliverPackages(truckList,delayedPackages):
#     """
#     Function to deliver packages for all trucks in the provided list.
#
#     Args:
#         truckList (list): A list of Truck objects that need to deliver their loaded packages.
#     Notes:
#         - This function assumes that all trucks in `truckList` have already been loaded with packages.
#         - Each truck's status (including mileage, time, and package status) will be updated during the delivery process.
#     """
#     for truck in truckList:
#         deliverTruckPackages(truck, delayedPackages)
#
#         # If any delayed packages are still left, have the truck return to the hub to load them
#         if delayedPackages:
#             returnToHubAndLoadDelayedPackages(truck, delayedPackages)
#
#             # Once delayed packages are loaded, deliver them
#             deliverTruckPackages(truck, delayedPackages)


def userInteractionLoop(truckList, hashTable):
    """
    Function to handle user interaction for managing package deliveries.

    Args:
        truckList (list): A list of Truck objects containing information about the loaded packages.
        hashTable (HashTable): A hash table containing package data for lookup.
    """
    while True:
        printUI()
        userChoice = input("Enter your choice: ")

        if userChoice == '1':
            printCalculateTotalMileage(truckList)
            # Print all package statuses and total mileage for all trucks
            printHeader()

            # Iterate over each package loaded onto the truck
            for packageIndex in range(1, 41):
               print(hashTable.lookUp(packageIndex))
            print()
                # for package in truck.packages:
                #     if package:
                #         print(f"{package.packageID}, {package.deliveryAddress}, {package.city}, {package.state}, "
                #               f"{package.zip}, {package.deliveryDeadline}, {package.packageWeight}, "
                #               f"{package.pageSpecialNotes}, {package.deliveryStatus}, "
                #               f"{package.deliveryTime if package.deliveryTime else 'Not Delivered'}")
                #     else:
                #         print(f"Package not found for Truck {truck.truckId}")

        elif userChoice == '2':
            # Get a single package status
            try:
                packageID = int(input("Enter package ID: "))
                currentTime = input("Enter the time to get package status (HH:MM): ")

                # Parse user input into a timedelta
                currentTime = timedelta(hours=int(currentTime.split(':')[0]), minutes=int(currentTime.split(':')[1]))

                # Lookup the package in the hash table
                package = hashTable.lookUp(packageID)

                if package:
                    # Determine the status based on the time
                    if package.deliveryTime and currentTime >= package.deliveryTime:
                        packageStatus = "Delivered"
                    elif currentTime < timedelta(hours=8):  # Before trucks left the hub
                        packageStatus = "At Hub"
                    elif package.deliveryTime and currentTime < package.deliveryTime:
                        packageStatus = "En Route"
                    else:
                        packageStatus = "At Hub"  # Default status if none of the above apply

                    # Print package information
                    print(f"\nStatus at {currentTime}: {packageStatus}\n")
                    printHeader()
                    print(package,"\n")
                else:
                    print(f"Package ID {packageID} not found.")

            except ValueError:
                print("Invalid input. Please enter a valid package ID.")

        elif userChoice == '3':
            # Get all package statuses at a specific time
            currentTimeInput = input("Enter the time to get package status (HH:MM): ")

            try:
                # Manually parse the input time
                timeParts = currentTimeInput.split(':')
                if len(timeParts) != 2:
                    raise ValueError("Invalid time format")

                hours = int(timeParts[0])
                minutes = int(timeParts[1])

                # Create a timedelta object for the specified time
                currentTime = timedelta(hours=hours, minutes=minutes)

                # Create the hash table and load package data
                hashTable = createPackageData()

                # Create trucks
                truckList = initializeTrucks(3, hashTable)
                # TODO delete later print(distanceBetween('1488 4800 S', '1488 4800 S'))
                # Load packages into trucks
                loadPackagesIntoTrucks(hashTable, truckList)

                # Deliver packages for each truck in the truckList
                for truck in truckList:
                    deliverTruckPackagesUntil(truck,currentTime)

                printCalculateTotalMileage(truckList)

                # Print header
                printHeader()

                # Iterate over each package loaded onto the truck
                for packageID in range(1, 41):
                    package = hashTable.lookUp(packageID)
                    print(package)
            except ValueError:
                print("Invalid input. Please enter the time in HH:MM format.")

        elif userChoice == '4':
            # Exit the program
            print("Exiting the program.")
            break

        else:
            print("Invalid choice, please enter a number between 1 and 4.")


def printCalculateTotalMileage(truckList):
    truckTotalMileage = 0
    for truck in truckList:
        truckTotalMileage += truck.totalMileage
        # TODO delete later for debugging purposes only
        # print(f"\nTruck {truck.truckId} total mileage: {truck.totalMileage:.2f} miles")
    print(f"\nTrucks total mileage: {truckTotalMileage:.2f} miles\n")


def printHeader():
    print()
    print(
        "PackageID  Address                                   City                State      Zip        Deadline        Weight    Special Notes         Status                    DeliveryTime")
    print(
        "----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")

def findDelayedPackages(hashTable, totalPackages=40):
    """
    Finds all delayed packages based on their arrival time.

    Args:
        hashTable (HashTable): Hash table containing all package information.
        totalPackages (int): Total number of packages. Default is 40.

    Returns:
        list: List of packages that are delayed and have specific arrival times.
    """
    delayedPackages = []
    for packageID in range(1, totalPackages + 1):
        package = hashTable.lookUp(packageID)
        if package and package.arrivalTime:  # If the package has a delayed arrival time
            delayedPackages.append(package)
    return delayedPackages

def main():
    # Create the hash table and load package data
    hashTable = createPackageData()

    # Create trucks
    truckList = initializeTrucks(3, hashTable)

    # Load packages into trucks
    loadPackagesIntoTrucks(hashTable, truckList)

    # Find delayed packages
    delayedPackages = findDelayedPackages(hashTable)

    # Deliver packages for each truck that are not delayed packages
    deliverPackages(truckList)

    # Deliver delayed packages
    for truck in truckList:
        # Load delayed packages that are now available to be loaded
        newlyAvailablePackages = [pkg for pkg in delayedPackages if pkg.arrivalTime <= truck.currentTime]
        if newlyAvailablePackages:
            for pkg in newlyAvailablePackages:
                if len(truck.packages) < truck.capacity:
                    truck.loadPackage(pkg)
                    delayedPackages.remove(pkg)

        # Deliver the loaded delayed packages
        deliverTruckPackages(truck)

   # deliverPackages(truck.hashTable.lookUp(9))


    # User interaction loop
    userInteractionLoop(truckList, hashTable)


# Run the main function
if __name__ == '__main__':
    main()
