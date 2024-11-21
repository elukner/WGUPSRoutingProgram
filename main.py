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
    #     print(hashTable.lookUp(packageIndex))

    # Load data from CSV files
    loadDistanceData('distanceCSV.csv')
   #todo delete later
    print(distanceData)
    loadAddressData('addressCSV.csv')
    #todo delete later
    print(addressData)
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


def userInteractionLoop(truckList, hashTable):
    """
    Function to handle user interaction for managing package deliveries.

    Args:
        truckList (list): A list of Truck objects containing information about the loaded packages.
        hashTable (HashTable): A hash table containing package data for lookup.
    """
    while True:
        printUI()
        user_choice = input("Enter your choice: ")

        if user_choice == '1':
            # Print all package statuses and total mileage for all trucks
            for truck in truckList:
                print(f"Truck {truck.truckId} total mileage: {truck.totalMileage:.2f} miles")
                print("Packages on Truck:")
                for package in truck.packages:
                    print(
                        "PackageID, Address, City, State, Zip, Delivery Deadline, Mass KILO, PageSpecial Notes, Status, DeliveryTime")
                    print(package)

        elif user_choice == '2':
            # Get a single package status
            try:
                package_id = int(input("Enter package ID: "))
                package = hashTable.lookUp(package_id)
                if package:
                    print(
                        "PackageID, Address, City, State, Zip, Delivery Deadline, Mass KILO, PageSpecial Notes, Status, DeliveryTime")
                    print(package)
                else:
                    print(f"Package ID {package_id} not found.")
            except ValueError:
                print("Invalid input. Please enter a valid package ID.")

        elif user_choice == '3':
            # Get all package statuses at a specific time
            current_time = input("Enter the time to get package status (HH:MM): ")
            # This part could involve checking which packages are delivered at the specified time
            print("Feature under development.")  # TODO need to finish

        elif user_choice == '4':
            # Exit the program
            print("Exiting the program.")
            break

        else:
            print("Invalid choice, please enter a number between 1 and 4.")


def main():
    # Create the hash table and load package data
    hashTable = createPackageData()

    # Create trucks
    truckList = initializeTrucks(3, hashTable)

    # Load packages into trucks
    loadPackagesIntoTrucks(hashTable, truckList)

    # Deliver packages for each truck in the truckList
    deliverPackages(truckList)

    # User interaction loop
    userInteractionLoop(truckList, hashTable)


# Run the main function
if __name__ == '__main__':
    main()
