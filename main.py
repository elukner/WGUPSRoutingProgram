# TODO don't submit to github this part
# Create an identifying comment within the first line of a file named “main.py” that includes your student ID.

from Package import *
from HashTable import *
from Truck import *
from CSV import *

distanceData = []
addressData = []


def loadDistanceData(fileName):
    """
    This function reads distance data from the provided CSV file and appends each row to the distanceData list.

    Steps:
    1. Reads the distance data from the distanceCSV file.
    2. Appends each row to the distanceData list.

    :param fileName: The name of the CSV file containing distance data.
    :return: A 2D list containing distances between addresses.
    """
    currentDistanceData = distanceData  # Create distanceData List

    with (open(fileName) as csvfile):
        distanceDataReader = csv.reader(csvfile, delimiter=',')

        # Skip the first row
        next(distanceDataReader)

        for row in distanceDataReader:
            # Convert each distance value to float, replacing empty strings with 0.0
            cleanedRow = []
            for value in row[1:]:
                try:
                    cleanedRow.append(float(value))
                except ValueError:
                    cleanedRow.append(0.0)

            #print(cleanedRow) TODO delete later
            currentDistanceData.append(cleanedRow)
        #print(currentDistanceData) TODO delete later
    return currentDistanceData

def loadAddressData(fileName):
    """
    This function reads address data from the provided CSV file and appends each address to the addressData list.

    Steps:
    1. Reads the address data from the addressCSV file.
    2. Appends each address to the addressData list.

    :param fileName: The name of the CSV file containing address data.
    :return: A list containing all addresses from the CSV file.
    TODO emailed questions about "For the loadAddressData(addressData) and loadDistanceData(distanceData)
    funtions in the nearest neighbor implementation for part C are these meant to
    only read one line or the entire file because I was setting it up so that it reads the whole file. "
    """
    currentAddressData = addressData

    with (open(fileName) as csvfile):
        addressDataReader = csv.reader(csvfile, delimiter=',')

        #Skip the first row
        next(addressDataReader)

        for row in addressDataReader:
            # Make sure the row has at least one element to avoid index out of range errors
            if len(row) > 0:
                # Extract the address from the first column (index 0)
                address = row[0].strip()  # Remove any leading or trailing whitespace
                if address:  # Make sure address is not empty
                    addressData.append(address)
                    #print(address) #TODO delete later

    #print(currentAddressData) TODO delete later
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
        next(packageData)  # skip the header row
        for package in packageData:
            packageID = int(package[0])
            deliveryAddress = package[1]
            city = package[2]
            state = package[3]
            zip = package[4]
            deliveryDeadline = package[5]
            packageWeight = package[6]
            pageSpecialNotes = package[7]
            deliveryStatus = "At Hub"  # Setting initial status to be "At Hub"

            # calculate the distance from teh hub to the package address
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
            hashTable.insert(packageID, package)


# TODO + truckLoadPackages()
    # C.3) Function to load packages into Trucks:
    # 12-Define truckLoadPackages() //DONE
    def truckLoadPackages():
        pass  # TODO delete later

    # 13-Load Trucks based on assumptions provided
    # (ex. Truck-2 must have some packages, some packages go together,
    # some packages are delayed, ...)
    # 14-And closest addresses/packages until there is 16 packages in a Truck
    # i.e. Load manually/heuristically or Loop package addresses
    # and call minDistanceFrom(fromAddress, truckPackages)
    # for all the addresses in the Truck not visited yet

    # TODO + truckDeliverPackages(truck)
    # D.1) Function to deliver packages in a Truck:
    # 15-Define truckDeliverPackages(truck)
    def truckDeliverPackages(truck):
        pass  # TODO delete later
# 16-Loop truck package addresses
# and call minDistanceFrom(fromAddress, truckPackages)
# for all the addresses not visited yet
# D.2) Keep track of miles and time delivered: (remember funtion in package.py for update status)
# 17-Update delivery status and time delivered in Hash Table for the package
# delivered and keep up with total mileage and delivery times.
# i.e. How to keep track of the time?:
# timeToDeliver(h) = distance(miles)/18(mph) where 18 mph average Truck speed.
# time_obj = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s)).
# time_obj could be cumulated to keep track of time.

# TODO C.  Write an original program that will deliver all packages and meet all
# requirements using the attached supporting documents
# “Salt Lake City Downtown Map,” “WGUPS Distance Table,” and “WGUPS Package File.”
# D.  Provide an intuitive interface for the user to view the delivery status
# (including the delivery time) of any package at any time and the total mileage traveled by all trucks.
# (The delivery status should report the package as at the hub, en route,
# or delivered. Delivery status must include the time.)

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
    loadDistanceData('distanceCSV.csv')
    loadAddressData('addressCSV.csv')
#    hashTable = HashTable()
#    loadPackageData('packageCSV.csv', hashTable)
    printUI()
    # print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
