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
    :return: None
    """
    print(f'***************************************')
    print(f'1. Print All Package Status and Total Mileage')
    print(f'2. Get a Single Package Status with a Time')
    print(f'3. Get All Package Status with a Time')
    print(f'4. Exit the Program')
    print(f'***************************************')


def createPackageData():
    """
    Creates the hash table and loads package data
    :return: None
    """
    #
    hashTable = HashTable()
    loadPackageData('packageCSV.csv', hashTable)
    loadDistanceData('distanceCSV.csv')
    loadAddressData('addressCSV.csv')
    return hashTable


def initializeTrucks(numTrucks, hashTable):
    """
    Function to create and initialize a list of trucks.
    :param numTrucks: The number of trucks to be created.
    :param hashTable: Reference to the hash table for package status management.
    :return: list: A list of initialized Truck objects.
    """
    trucks = []

    # Create trucks based on the number specified
    for i in range(1, numTrucks + 1):
        truck = Truck(truckId=i, hashTable=hashTable)
        trucks.append(truck)

    return trucks


def loadPackagesIntoTrucks(hashTable, truckList, totalPackages=40):
    """
    Function to load packages into trucks using the nearest neighbor approach.
    :param hashTable: Hash table containing all package information.
    :param truckList: A list of Truck objects to load packages into.
    :param totalPackages: Total number of packages to be loaded. Default is 40.
    :return: list: Updated list of Truck objects with loaded packages.
    """
    # Get all packages from the hash table based on the package IDs
    packages = [hashTable.lookUp(packageID) for packageID in range(1, totalPackages + 1)]

    # Load packages into each truck
    for truck in truckList:
        truckLoadPackages(truck, packages)

    return truckList

def deliverPackages(truckList):
    """
    Function to deliver a list of packages to a truck.
    :param truckList: A list of Truck objects that need to deliver their loaded packages.
    :return: None
    """
    for truck in truckList:
        deliverTruckPackages(truck)



def userInteractionLoop(truckList, hashTable):
    """
    Function to handle user interaction for managing package deliveries.
    :param truckList: A list of Truck objects containing information about the loaded packages.
    :param hashTable: A hash table containing package data for lookup.
    :return: None
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
                    print(f"\nStatus at {currentTime}: { packageStatus}\n")
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
    """
    Function to calculate the total mileage of a truck.
    :param truckList: A list of Truck objects containing information about the loaded packages.
    :return: None
    """
    truckTotalMileage = 0
    for truck in truckList:
        truckTotalMileage += truck.totalMileage
    print(f"\nTrucks total mileage: {truckTotalMileage:.2f} miles\n")


def printHeader():
    """
    Helper function that is called in the user interface to print the header for the list of packages.
    :return: None
    """
    print()
    print(
        "PackageID  Address                                   City                State      Zip        Deadline        Weight    Special Notes         Status                    DeliveryTime")
    print(
        "----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")

def findDelayedPackages(hashTable, totalPackages=40):
    """
    Finds all delayed packages based on their arrival time.
    :param hashTable: Hash table containing all package information.
    :param totalPackages: Total number of packages. Default is 40.
    :return: list: List of packages that are delayed and have specific arrival times.
    """
    delayedPackages = []
    for packageID in range(1, totalPackages + 1):
        package = hashTable.lookUp(packageID)
        if package and package.arrivalTime:  # If the package has a delayed arrival time
            delayedPackages.append(package)
    return delayedPackages

def main():
    """
    Main function to manage the process of loading packages, delivering them, and handling user interaction.

    Steps:
    1. Create the hash table and load package data.
    2. Create trucks and initialize them.
    3. Load packages into trucks using loading rules.
    4. Identify and deliver delayed packages when available.
    5. Deliver packages using nearest neighbor algorithm.
    6. Provide an interface for user interactions.

    :return: None
    """
    hashTable, truckList = runRouteUntil()

    # deliverPackages(truck.hashTable.lookUp(9))


    # User interaction loop
    userInteractionLoop(truckList, hashTable)


def runRouteUntil():
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
        # returnToHubAndLoadDelayedPackages(truck, delayedPackages)
        # Load delayed packages that are now available to be loaded
        newlyAvailablePackages = [pkg for pkg in delayedPackages if pkg.arrivalTime <= truck.currentTime]
        if newlyAvailablePackages:
            for pkg in newlyAvailablePackages:
                if len(truck.packages) < truck.capacity:
                    truck.loadPackage(pkg)
                    delayedPackages.remove(pkg)

        # Deliver the loaded delayed packages
        deliverTruckPackages(truck)
    return hashTable, truckList


# Run the main function
if __name__ == '__main__':
    main()
