# Student ID: 12345678  # Replace with your actual student ID; this line identifies the submission.

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
    for packageIndex in range(1, 41):
        print(hashTable.lookUp(packageIndex))

    # Load data from CSV files
    loadDistanceData('distanceCSV.csv')
    print(distanceData)
    loadAddressData('addressCSV.csv')
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


def main():
    # Create the hash table and load package data
    hashTable = createPackageData()

    # Create trucks
    truckList = initializeTrucks(3, hashTable)

    # Load packages into trucks
    packages = [hashTable.lookUp(packageID) for packageID in range(1, 41)]  # Assume there are 40 packages
    # truckLoadPackages(truck1, packages)
    # truckLoadPackages(truck2, packages)
    # truckLoadPackages(truck3, packages)

    # check to see if packages are loaded in trucks TODO delete later
    # truckList = [truck1, truck2, truck3]
    # for truck in truckList:
    #     print('truck: ', truck.truckId, 'packages: ')
    #     for package in truck.packages:
    #         print(package)
    #         print()
    # TODO el packages are not loading into trucks


    print(distanceBetween('1060 Dalton Ave S','1330 2100 S'))
    # Deliver packages
    truckDeliverPackages(truck1)
    truckDeliverPackages(truck2)
    truckDeliverPackages(truck3)

    # Deliver packages for each truck in the truckList
    for truck in truckList:
        truckDeliverPackages(truck)

    # User interaction loop
    while True:
        printUI()
        user_choice = input("Enter your choice: ")
        if user_choice == '1':
           # for packageIndex in range(1, 41):
            #    print(hashTable.lookUp(packageIndex))
            # Print all package statuses and total mileage for all trucks
            for truck in [truck1, truck2, truck3]:
                print(f"Truck {truck.truckId} total mileage: {truck.totalMileage:.2f} miles")
                for package in truck.packages:
                    print(
                        f"PackageID, Address, City, State, Zip, Delivery Deadline, Mass KILO, PageSpecial Notes, Status, DeliveryTime")
                    print(package)
        elif user_choice == '2':
            # Get a single package status
            package_id = int(input("Enter package ID: "))
            package = hashTable.lookUp(package_id)
            if package:
                print(f"PackageID, Address, City, State, Zip, Delivery Deadline, Mass KILO, PageSpecial Notes, Status, DeliveryTime")
                print(package)
            else:
                print(f"Package ID {package_id} not found.")
        elif user_choice == '3':
            # Get all package statuses
            current_time = input("Enter the time to get package status (HH:MM): ")
            # This part could involve checking which packages are delivered at the specified time
            print("Feature under development.") #TODO need to finish
        elif user_choice == '4':
            # Exit the program
            print("Exiting the program.")
            break
        else:
            print("Invalid choice, please enter a number between 1 and 4.")




# Run the main function
if __name__ == '__main__':
    main()
