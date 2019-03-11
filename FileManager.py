import classes
def readFile(filename):
    theFile = open(filename, "r")
    line = theFile.readline()
    row, columns , vehicles, numberOfRides, bonus, steps = [int(i) for i in  line.split(" ")]
    
    allLines = theFile.readlines()
    rideNumber = 0 
    
    rides =  []
    for x in allLines:
        splittedLine = x.split(" ")
        rides.append( classes.Ride([int(splittedLine[0]), int(splittedLine[1])],  [int(splittedLine[2]), int(splittedLine[3])], int(splittedLine[4]), int(splittedLine[5]), rideNumber))
        rideNumber +=1

    return  row, columns , vehicles, numberOfRides, bonus, steps, rides
















