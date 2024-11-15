# This Python file contains supporting functions for the WGUPS Routing Program.
from main import addressData, distanceData


# Function to return the distance between two addresses
def distanceBetween(address1, address2):
    """
    Function to return the distance between two addresses.
    :param address1: The starting address.
    :param address2: The destination address.
    :return: Distance in miles between address1 and address2.
    """
    try:
        index1 = addressData.index(address1)
        index2 = addressData.index(address2)
        return distanceData[index1][index2]
    except ValueError:
        # If the address is not found, return a large value (inf) to indicate it is unreachable
        return float('inf')


# Function to find min distance/address
def minDistanceFrom(fromAddress, truckPackages):
    """
    Function to find the package with the minimum distance from the given address.
    :param fromAddress: The address to calculate distances from.
    :param truckPackages: List of packages that need to be delivered.
    :return: The package object with the minimum distance to fromAddress.
    """
    # If truckPackages is empty, return None
    if not truckPackages:
        return None

    minDistance = float("inf")
    closestPackage = None

    # Loop through all packages in the truck to find the closest package
    for truckPackage in truckPackages:
        distance = distanceBetween(fromAddress, truckPackage.deliveryAddress)

        # Skip the distance if it is 'inf', meaning the address is unreachable
        if distance == float('inf'):
            continue

        if distance < minDistance:
            minDistance = distance
            closestPackage = truckPackage

    return closestPackage


# Function to calculate time to deliver
def timeToDeliver(distance):
    """
    Function to calculate the time required to deliver based on distance.
    Assumes an average speed of 18 mph.
    :param distance: Distance that will be traveled in miles.
    :return: Time in hours required to travel the given distance.
    """
    averageSpeedMph = 18  # Assumption that trucks travel at an average speed of 18 miles per hour
    return distance / averageSpeedMph
