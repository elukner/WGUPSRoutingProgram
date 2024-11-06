#TODO loadPackageData()
#TODO 3-Create loadPackageData(HashTable) to
# - read packages from packageCSV file (see C950 - Webinar-2 - Getting Greedy, who moved my data  webinar)
# - update Package object
# - insert Package object into HashTable with the key=PackageID and Item=Package

#TODO loadDistanceData()
# B.1) Upload Distances:
# 4-Create distanceData List
# 5-Define loadDistanceData(distanceData) to read distanceCSV file
# - read distances from distanceCSV file; row by row
# - append row to distanceData (two-dimensional list.
# See C950 WGUPS Distance Table Matrix)

#TODO loadAddressData()
# B.2) Upload Addresses:
# 6-Create addressData List
# 7-Define loadAddressData(addressData) to read addressCSV file
# - read only addresses from addressCSV file
# - append address to addressData.

#TODO truckLoadPackages()
#TODO truckDeliverPackages()

#TODO UI interaction
# 18-Create an UI to interact and report the results based on the requirements.
# Menu Options:
# ***************************************
# 1. Print All Package Status and Total Mileage
# 2. Get a Single Package Status with a Time
# 3. Get All Package Status with a Time
# 4. Exit the Program
# ***************************************


# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
