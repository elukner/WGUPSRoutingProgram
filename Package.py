class Package:
    """
    Represents a package for delivery, containing all the relevant information needed
    to track the package throughout the delivery process.

    Attributes:
        packageID (int): The unique identifier for the package.
        deliveryAddress (str): The delivery address of the package.
        city (str): The city where the package will be delivered.
        state (str): The state where the package will be delivered.
        zip (str): The zip code of the delivery address.
        deliveryDeadline (str): The time by which the package should be delivered (e.g., '10:30 AM', 'EOD').
        packageWeight (float): The weight of the package in kilograms.
        pageSpecialNotes (str): Any special instructions for the package (e.g., 'Leave at back door').
        deliveryStatus (str): The current status of the package (default is "At Hub").
        deliveryTime (timedelta or None): The time when the package was delivered (default is None).
    """
    def __init__(self, packageID, deliveryAddress, city, state, zip, deliveryDeadline,
                 packageWeight, pageSpecialNotes, deliveryStatus="At Hub", deliveryTime=None):
        """
        Initializes a Package instance.

        Args:
            packageID (int): The unique identifier for the package.
            deliveryAddress (str): The delivery address of the package.
            city (str): The city where the package will be delivered.
            state (str): The state where the package will be delivered.
            zip (str): The zip code of the delivery address.
            deliveryDeadline (str): The time by which the package must be delivered.
            packageWeight (float): The weight of the package in kilograms.
            pageSpecialNotes (str): Special notes or instructions regarding the package.
            deliveryStatus (str, optional): The current status of the package.
                Defaults to "At Hub". Possible values include "At Hub", "En Route", and "Delivered".
            deliveryTime (timedelta or None, optional): The time when the package is delivered.
                Defaults to None until the package is delivered.

        Attributes Initialized:
            packageID: Stores the unique identifier for the package.
            deliveryAddress: Stores the delivery address.
            city: Stores the delivery city.
            state: Stores the delivery state.
            zip: Stores the zip code of the delivery address.
            deliveryDeadline: Stores the delivery deadline time.
            packageWeight: Stores the package weight in kilograms.
            pageSpecialNotes: Stores any special notes regarding the package.
            deliveryStatus: Indicates the current status of the package (initially set to "At Hub").
            deliveryTime: Represents the time the package was delivered (initially None).
        """
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

    def updateStatus(self, status:str, deliveryTime=None):
        """
        Update the delivery status of the package.
        :param status: Current status of the package (e.g., 'At Hub', 'En Route', 'Delivered').
        :return: Time of delivery
        """
        self.deliveryStatus = status
        if ("Delivered" in status) and deliveryTime:
            self.deliveryTime = deliveryTime

    def __str__(self):
        """
        Function that returns a string representation of the package.
        :return: string representation of the package
        """
        truncatedNotes = (self.pageSpecialNotes[:17] + "...") if len(self.pageSpecialNotes) > 20 else self.pageSpecialNotes
        return (
            f"{str(self.packageID):<10} {self.deliveryAddress:<40} {self.city:<20} {self.state:<10} {self.zip:<10} "
            f"{self.deliveryDeadline:<15} {str(self.packageWeight):<10} {truncatedNotes:<20} {self.deliveryStatus:<25} "
            f"{str(self.deliveryTime) if self.deliveryTime else 'Not Delivered':<20}"
        )
