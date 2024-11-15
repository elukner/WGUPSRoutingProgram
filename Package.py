# TODO 2-Create Package and Truck objects and have packageCSV and distanceCSV and addressCSV files ready
# TODO + packageID
# TODO + address
# TODO + city
# TODO + state
# TODO + zip
# TODO + deliveryDeadline
# TODO + massKilo
# TODO + pageSpecialNotes
# TODO + status
# TODO + deliveryTime
# TODO + updateStatus(status)
class Package:
    def __init__(self, packageID, deliveryAddress, city, state, zip, deliveryDeadline,
                 packageWeight, pageSpecialNotes, deliveryStatus="At Hub", deliveryTime=None):
        self.packageID = packageID
        self.deliveryAddress = deliveryAddress
        self.city = city
        self.state = state
        self.zip = zip
        self.deliveryDeadline = deliveryDeadline
        self.packageWeight = packageWeight
        self.pageSpecialNotes = pageSpecialNotes
        self.deliveryStatus = deliveryStatus  # Initial status  (i.e., at the hub, en route, or delivered)
        self.deliveryTime = deliveryTime  # Time when the package is delivered

    # TODO + updateStatus(status)
    def updateStatus(self, status, deliveryTime=None):
        """
        Update the delivery status of the package.
        :param status: Current status of the package (e.g., 'At Hub', 'En Route', 'Delivered').
        :return: Time of delivery
        """
        self.deliveryStatus = status
        if status == "Delivered" and deliveryTime:
            self.deliveryTime = deliveryTime

    def __str__(self):
        """
        Function that returns a string representation of the package.
        :return: string representation of the package
        """
        return ( #TODO el: update this to show what each item means so someone who didn't write the code can tell what each item is.  This will help you debug too.
            f"{self.packageID}, {self.deliveryAddress}, {self.city}, {self.state}, {self.zip}, "
            f"{self.deliveryDeadline}, {self.packageWeight}, {self.pageSpecialNotes}, {self.deliveryStatus}, "
            f"{self.deliveryTime if self.deliveryTime else 'Not Delivered'}")
