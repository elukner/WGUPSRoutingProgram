# Student ID: 12345678  # Replace with your actual student ID; this line identifies the submission.

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
                address = row[0].strip()  # Extract the address from the first column (index 0)
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
    # TODO el: the packages get removed from remaining_packages but don't get removed from the global packages variable.  So then all the packages get sent to the next truck instead of just the ones that are left.



def truckDeliverPackages(truck):
    """
    Delivers all packages loaded on the truck.
    """
    truck.deliverPackages()


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


def main():
    # Load data from CSV files
    loadDistanceData('distanceCSV.csv')
    loadAddressData('addressCSV.csv')

    # Create the hash table and load package data
    hashTable = HashTable()
    loadPackageData('packageCSV.csv', hashTable)

    # Create trucks
    truck1 = Truck(1, hashTable)
    truck2 = Truck(2, hashTable)
    truck3 = Truck(3, hashTable)

    # Load packages into trucks
    packages = [hashTable.lookUp(packageID) for packageID in range(1, 41)]  # Assume there are 40 packages
    truckLoadPackages(truck1, packages)
    truckLoadPackages(truck2, packages)
    truckLoadPackages(truck3, packages)

    # Deliver packages
    truckDeliverPackages(truck1)
    truckDeliverPackages(truck2)
    truckDeliverPackages(truck3)

    # User interaction loop
    while True:
        printUI()
        user_choice = input("Enter your choice: ")
        if user_choice == '1':
            # Print all package statuses and total mileage for all trucks
            for truck in [truck1, truck2, truck3]:
                print(f"Truck {truck.truckId} total mileage: {truck.totalMileage:.2f} miles")
                for package in truck.packages:
                    print(package)
        elif user_choice == '2':  #TODO el: print the column headers for each of the rows in the printed data.  I don't know what each item represents.
            # Get a single package status
            package_id = int(input("Enter package ID: "))
            package = hashTable.lookUp(package_id)
            if package:
                print(package)
            else:
                print(f"Package ID {package_id} not found.")
        elif user_choice == '3':
            # Get all package statuses
            current_time = input("Enter the time to get package status (HH:MM): ")
            # This part could involve checking which packages are delivered at the specified time
            print("Feature under development.")
        elif user_choice == '4':
            # Exit the program
            print("Exiting the program.")
            break
        else:
            print("Invalid choice, please enter a number between 1 and 4.")


# Run the main function
if __name__ == '__main__':
    main()
