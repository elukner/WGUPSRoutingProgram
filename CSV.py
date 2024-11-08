# TODO this python file will be used to hold the
# supporting functions distanceBetween(), minDistanceFrom(), and timeToDeliver()


# TODO distanceBetween(address1, address2)
# C.1) Function to return the distance between two addresses:
# 8-Define distanceBetween(address1, address2)
# 9-Return distanceData[addressData.index(address1)][addressData.index(address2)]
# i.e. distances between addresses can be accessed via distanceData[i][j];
def distanceBetween(address1, address2):
    pass  # TODO delete later

# C.2) Function to find min distance/address:
# 10-Define minDistanceFrom(fromAddress, truckPackages)
# 11-Return min distance address to fromAddress
# i.e. call distanceBetween(address1, address2) in a loop for all the addresses in the Truck
def minDistanceFrom(fromAddress, truckPackages):
    """
    Function to find min distance/address
    :param fromAddress: The address to calculate distances from.
    :param truckPackages: List of packages that need to be delivered.
    :return: Return min distance address to fromAddress
    """
    minDistance = float("inf")
    closestPackage = None

    for truckPackage in truckPackages:
        #i.e. call distanceBetween(address1, address2) in a loop for all the addresses in the Truck
        distance = distanceBetween(fromAddress, truckPackage.deliveryAddress)
        if distance < minDistance:
            minDistance = distance
            closestPackage = truckPackage

    return closestPackage

def timeToDeliver(distance):
    """
    function calculates distance(miles)/18(mph) where 18 mph average Truck speed
    :param distance: Distance that will be traveled in miles.
    :return: Time in hours required to travel the given distance.
    """
    averageSpeedMph = 18 #Assumption that trucks travel at an average speed of 18 miles per hour
    return distance/averageSpeedMph