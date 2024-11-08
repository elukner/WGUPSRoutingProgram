# TODO don't submit to github this part
# Create an identifying comment within the first line of a file named “main.py” that includes your student ID.

from HashTable import *
from Package import *
from HashTable import *
from Truck import *
from CSV import *

# TODO C.  Write an original program that will deliver all packages and meet all
# requirements using the attached supporting documents
# “Salt Lake City Downtown Map,” “WGUPS Distance Table,” and “WGUPS Package File.”
# D.  Provide an intuitive interface for the user to view the delivery status
# (including the delivery time) of any package at any time and the total mileage traveled by all trucks.
# (The delivery status should report the package as at the hub, en route,
# or delivered. Delivery status must include the time.)


# TODO loadPackageData(HashTable)
# TODO 3-Create loadPackageData(HashTable) to
# - read packages from packageCSV file (see C950 - Webinar-2 - Getting Greedy, who moved my data  webinar)
# - update Package object
# - insert Package object into HashTable with the key=PackageID and Item=Package
def loadPackageData(fileName):
    with open(fileName) as packageCSV:
        packageData = csv.reader(packageCSV, delimiter=',')
        next(packageData)
        for package in packageData:
            packageID = int(package[0])
            deliveryAddress = package[1]
            city = package[2]
            state = package[3]
            zip = package[4]
            deliveryDeadline = package[5]
            packageWeight = package[6]
            pageSpecialNotes = package[7]
            deliveryStatus = "not delivered" #what do I set this too?
            deliveryTime = timeToDeliver() #where do I get distance from?

            # movie object
            package = Package(packageID, deliveryAddress, city, state, zip,deliveryDeadline,
                              packageWeight, pageSpecialNotes, deliveryStatus, deliveryTime)
            # print(m)

            # insert it into the hash table
            HashTable.insert(packageID,m)


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
    printUI()
    # print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
