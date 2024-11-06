#TODO 2-Create Package and Truck objects
# and have packageCSV and distanceCSV and addressCSV files ready

#TODO + truckID
#TODO + packages: List[Package]

#TODO + truckLoadPackages(package?<-this is not in implementation steps)
# C.3) Function to load packages into Trucks:
# 12-Define truckLoadPackages()
# 13-Load Trucks based on assumptions provided
# (ex. Truck-2 must have some packages, some packages go together,
# some packages are delayed, ...)
# 14-And closest addresses/packages until there is 16 packages in a Truck
# i.e. Load manually/heuristically or Loop package addresses
# and call minDistanceFrom(fromAddress, truckPackages)
# for all the addresses in the Truck not visited yet

#TODO + deliverPackage()