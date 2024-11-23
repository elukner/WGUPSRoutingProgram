from datetime import timedelta


class Package:
    """
    Represents a package for delivery, containing all the relevant information needed
    to track the package throughout the delivery process.
    """

    def __init__(self, packageID, deliveryAddress, city, state, zip, deliveryDeadline,
                 packageWeight, pageSpecialNotes, deliveryStatus="At Hub", deliveryTime=None):
        """
        Initializes a Package instance.

        :param packageID: The unique identifier for the package.
        :param deliveryAddress: The delivery address of the package.
        :param city: The city where the package will be delivered.
        :param state: The state where the package will be delivered.
        :param zip: The zip code of the delivery address.
        :param deliveryDeadline: The time by which the package must be delivered.
        :param packageWeight: The weight of the package in kilograms.
        :param pageSpecialNotes: Special notes or instructions regarding the package.
        :param deliveryStatus: The current status of the package.
        :param deliveryTime: The time when the package is delivered.
        """
        self.packageID = packageID
        self.deliveryAddress = deliveryAddress
        self.city = city
        self.state = state
        self.zip = zip
        self.deliveryDeadline = deliveryDeadline
        self.packageWeight = packageWeight
        self.pageSpecialNotes = pageSpecialNotes
        self.deliveryStatus = deliveryStatus
        self.deliveryTime = deliveryTime

        # Additional attributes based on special notes
        self.allowedTruck = None  # Truck restriction, if any
        self.groupDependency = []  # List of package IDs that must be delivered together
        self.arrivalTime = None  # Time when the package arrives at the hub
        self.addressCorrectionNeeded = False  # Flag for incorrect address

        self.parseSpecialNotes()  # Parse the special notes during initialization

    def parseSpecialNotes(self):
        """
        Parses the special notes to set additional attributes like allowedTruck,
        groupDependency, arrivalTime, or addressCorrectionNeeded.
        :return: None
        """
        if "Can only be on truck" in self.pageSpecialNotes:
            # Extract truck number
            truckNumber = int(self.pageSpecialNotes.split("truck")[1].strip())
            self.allowedTruck = truckNumber

        if "Must be delivered with" in self.pageSpecialNotes:
            # Extract package IDs that this package must be delivered with
            ids = self.pageSpecialNotes.split("Must be delivered with")[1].strip().split(',')
            self.groupDependency = [int(id.strip()) for id in ids]

        if "Delayed on flight" in self.pageSpecialNotes:
            # Extract delay time from the note
            delayTimeString = self.pageSpecialNotes.split("until")[1].replace('am', ' ').strip()
            hours = int(delayTimeString.split(':')[0])
            minutes = int(delayTimeString.split(':')[1])
            self.arrivalTime = timedelta(hours=hours, minutes=minutes)

        if "Wrong address listed" in self.pageSpecialNotes:
            self.addressCorrectionNeeded = True

    def updateStatus(self, status: str, deliveryTime=None):
        """
        Updates the status of the package.
        :param status: The status of the package.
        :param deliveryTime: The time when the package is delivered.
        :return: None
        """
        self.deliveryStatus = status
        if ("Delivered" in status) and deliveryTime:
            self.deliveryTime = deliveryTime

    def __str__(self):
        """
        Function that returns a string representation of the package.
        :return: string representation of the package
        """
        truncatedNotes = (self.pageSpecialNotes[:17] + "...") if len(
            self.pageSpecialNotes) > 20 else self.pageSpecialNotes
        return (
            f"{str(self.packageID):<10} {self.deliveryAddress:<40} {self.city:<20} {self.state:<10} {self.zip:<10} "
            f"{self.deliveryDeadline:<15} {str(self.packageWeight):<10} {truncatedNotes:<20} {self.deliveryStatus:<25} "
            f"{str(self.deliveryTime) if self.deliveryTime else 'Not Delivered':<20}"
        )
