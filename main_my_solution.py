import FileManager
import classes
import math


currentStep = 0



def main():
    row, columns , numberOfVehicles, numberOfRides, bonus, steps, rides = FileManager.readFile(input("The file name: "))

    vehicles =  startVehicles( numberOfVehicles)
    vehicles = assignCar(vehicles, rides)
    printSelectedRoutes(vehicles)



def assignCar(vehicles, rides):
    distance = lambda cx,cy, sx,sy : math.fabs( float(cx -sx)) + math.fabs(float(cy- sy))
    
    for ride in rides:
        minimumDistace = 100000000
        finalCarNumber = -1
        finalCar = None
        rideStart = ride.start
        
        car = searchValidCarForRide(ride, vehicles)

    return vehicles

def printSelectedRoutes(vehicles):
    for car in vehicles:
        if car.assignedRides >=0:
            x = ""
            x +=str(car.assignedRides) + " "
            for ride in car.rides:
                x+= str(ride) +" "
            print(x)


def startVehicles(numberOfVehicles):
    number = 1
    vehicles = []
    for i in range(numberOfVehicles):
        vehicles.append(classes.car( [0,0], number))
        number +=1
    return vehicles


def searchValidCarForRide(ride, vehicles):
    distance = lambda cx,cy, sx,sy : math.fabs( float(cx -sx)) + math.fabs(float(cy- sy))
    finalCarEarlyArrive = None
    arriveTime = 1000000
    timeToWait = 1000000
    endingTime = 100000000
    theFinalDistanceToFinish = -1 
    theFinalDistanceToStart = -1
    for car in vehicles :
        theposition = car.pos
        rideStart = ride.start
        rideFinish = ride.end
        theCurrentDistanceToStart = distance(theposition[0],theposition[1], rideStart[0], rideStart[1])
        theCurrentDistanceToFinish = distance(rideStart[0], rideStart[1], rideFinish[0], rideFinish[1])
        if  (car.step + theCurrentDistanceToStart + theCurrentDistanceToFinish ) <= ride.latestFinish:
            if math.fabs(arriveTime) > math.fabs(float(ride.earlyStart - (car.step + theCurrentDistanceToStart))):
                arriveTime = float(ride.earlyStart - (car.step + theCurrentDistanceToStart))
                finalCarEarlyArrive = car
                theFinalDistanceToFinish = theCurrentDistanceToFinish    
                theFinalDistanceToStart = theCurrentDistanceToStart
        if arriveTime == 0 :
            break
    if finalCarEarlyArrive is not None:
        finalCarEarlyArrive.assignedRides += 1
        if arriveTime > 0:
            finalCarEarlyArrive.step = arriveTime + finalCarEarlyArrive.step + theFinalDistanceToStart + theFinalDistanceToFinish
        else : 
            finalCarEarlyArrive.step = finalCarEarlyArrive.step + theFinalDistanceToStart + theFinalDistanceToFinish

        finalCarEarlyArrive.rides.append(ride.rideNumber)
        finalCarEarlyArrive.pos = ride.end
        return finalCarEarlyArrive

main()






































