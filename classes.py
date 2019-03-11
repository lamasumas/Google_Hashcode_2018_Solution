





class car:
    def __init__(self, pos, carNumber):
        self.carNumber = carNumber
        self.pos = pos
        self.assignedRides = 0
        self.rides = []
        self.step = 0
    
    pass


class Ride:
    def __init__(self, start, end, earlyStart, latestFinish, rideNumber):
        self.start = start
        self.end= end
        self.earlyStart = earlyStart
        self.latestFinish = latestFinish
        self.rideNumber = rideNumber
    pass

