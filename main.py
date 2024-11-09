# TODO don't submit to github this part
# Create an identifying comment within the first line of a file named “main.py” that includes your student ID.

from HashTable import *
from Package import *
from HashTable import *
from Truck import *
from CSV import *

distanceData = [] #Create distanceData List
addressData = [] #Create addressData List

# TODO C.  Write an original program that will deliver all packages and meet all
# requirements using the attached supporting documents
# “Salt Lake City Downtown Map,” “WGUPS Distance Table,” and “WGUPS Package File.”
# D.  Provide an intuitive interface for the user to view the delivery status
# (including the delivery time) of any package at any time and the total mileage traveled by all trucks.
# (The delivery status should report the package as at the hub, en route,
# or delivered. Delivery status must include the time.)

# TODO loadDistanceData(distanceData)
# B.1) Upload Distances:
# 4-Create distanceData List
# 5-Define loadDistanceData(distanceData) to read distanceCSV file
# - read distances from distanceCSV file; row by row
# - append row to distanceData (two-dimensional list.
# See C950 WGUPS Distance Table Matrix)
def loadDistanceData(distanceData):
    pass  # TODO delete later


# TODO loadAddressData(addressData)
# B.2) Upload Addresses:
# 6-Create addressData List
# 7-Define loadAddressData(addressData) to read addressCSV file
# - read only addresses from addressCSV file
# - append address to addressData.
def loadAddressData(addressData):
    pass  # TODO delete later


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
        next(packageData) #skip the header row
        for package in packageData:
            packageID = int(package[0])
            deliveryAddress = package[1]
            city = package[2]
            state = package[3]
            zip = package[4]
            deliveryDeadline = package[5]
            packageWeight = package[6]
            pageSpecialNotes = package[7]
            deliveryStatus = "At Hub" # Setting initial status to be "At Hub"

            #calculate the distance from teh hub to the package address
            hubAddress = "Hub"
            try:
                indexFrom = addressData.index(hubAddress)
                indexTo = addressData.index(hubAddress)
                distance = distanceData[indexFrom][indexTo]
                deliveryTime = timeToDeliver(distance)
            except ValueError:
                # If address is not found, set deliveryTime to None
                deliveryTime = None

            # Create Package object
            # - insert Package object into HashTable with the key=PackageID and Item=Package
            package = Package(packageID, deliveryAddress, city, state, zip, deliveryDeadline,
                              packageWeight, pageSpecialNotes, deliveryStatus, deliveryTime)
            # print(package) TODO delete later?

            # Insert it into the hash table
            hashTable.insert(packageID,package)





# TODO truckLoadPackages() ?? does this function need to be here or only in truck object
# TODO truckDeliverPackages(truck) ?? does this function need to be here or only in truck object

# TODO UI interaction
# 18-Create an UI to interact and report the results based on the requirements.
# Menu Options:
# ***************************************
# 1. Print All Package Status and Total Mileage
# 2. Get a Single Package Status with a Time
# 3. Get All Package Status with a Time
# 4. Exit the Program
# ***************************************
def printUI():
    print(f'***************************************')
    print(f'1. Print All Package Status and Total Mileage')
    print(f'2. Get a Single Package Status with a Time')
    print(f'3. Get All Package Status with a Time')
    print(f'4. Exit the Program')
    print(f'***************************************')


# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
#    loadDistanceData('distanceCSV.csv') TODO uncomment when these functions are complete
#    loadAddressData('addressCSV.csv') TODO uncomment when these functions are complete
#    hashTable = HashTable() TODO uncomment when these functions are complete
#    loadPackageData('packageCSV.csv', hashTable) TODO uncomment when these functions are complete
    printUI()
    # print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
