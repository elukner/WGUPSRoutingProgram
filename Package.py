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
    def __init__(self, packageID, address, city, state, zip, deliveryDeadline,
                 massKilo, pageSpecialNotes, status="At Hub", deliveryTime=None):
        self.packageID = packageID
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deliveryDeadline = deliveryDeadline
        self.massKilo = massKilo
        self.pageSpecialNotes = pageSpecialNotes
        self.status = status  # Initial status
        self.deliveryTime = deliveryTime  # Time when the package is delivered

    # TODO + updateStatus(status)
    def updateStatus(self, status):
        pass  # TODO delete later

    def __str__(self):
        pass  # TODO delete later
