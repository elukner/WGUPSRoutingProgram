#TODO 2-Create Package and Truck objects
# and have packageCSV and distanceCSV and addressCSV files ready

#TODO + packages: List[Package] ??? Because step 4,6 lists

#TODO + truckLoadPackages()
# C.3) Function to load packages into Trucks:
# 12-Define truckLoadPackages()
# 13-Load Trucks based on assumptions provided
# (ex. Truck-2 must have some packages, some packages go together,
# some packages are delayed, ...)
# 14-And closest addresses/packages until there is 16 packages in a Truck
# i.e. Load manually/heuristically or Loop package addresses
# and call minDistanceFrom(fromAddress, truckPackages)
# for all the addresses in the Truck not visited yet

#TODO + truckDeliverPackages(truck)
# D.1) Function to deliver packages in a Truck:
# 15-Define truckDeliverPackages(truck)
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