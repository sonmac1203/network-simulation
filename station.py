import numpy as np
from constants import *

lambdaIndex = 0
seriesLen = LAMBDAS[lambdaIndex] * SIMULATIONTIME


def expo(num):
    return (-1 / SIMULATIONTIME) * np.log(1 - num)


class Station:
    def __init__(self):
        self.backOff = 0
        self.CW = MIN_CW
        self.successes = 0
        self.index = 0
        self.backOffFrozen = False

        # Generate random set for A and C
        uniformSet = np.random.uniform(0, 1, seriesLen)

        # Generate exponential set
        exponentialSet = [expo(i) for i in uniformSet]

        # Convert to slot
        slotsSet = [np.ceil(i / SLOTTIME) for i in exponentialSet]

        # Generate arrival times
        arrivalTimes = []
        for i in range(seriesLen):
            arrivalTimes.append(sum(slotsSet[: i + 1]))

        self.arrivals = arrivalTimes

    def getArrivals(self):
        return self.arrivals

    def setBackOff(self, value):
        self.backOff = value

    def getBackOff(self):
        randomNumber = np.random.randint(self.CW)
        if self.backOffFrozen is not True:
            self.setBackOff(randomNumber)
        return self.backOff

    def freezeBackOff(self):
        self.backOffFrozen = True

    def setCW(self, newCW):
        self.CW = newCW

    def doubleCW(self):
        factor = 1 if self.CW == MAX_CW else 2
        self.setCW(factor * self.CW)

    def resetCW(self):
        self.setCW(MIN_CW)

    def transmit(self, globalTime):
        totalTime = DIFS + self.backOff + FRAME + SIFS + ACK
        globalTime += totalTime
        return globalTime

    def setSuccesses(self, num):
        self.successes = num

    def recordASuccess(self):
        self.setSuccesses(self.successes + 1)

    def getSuccesses(self):
        return self.successes

    def getIndex(self):
        return self.index

    def jump(self):
        self.index += 1

    def collide(self, globalTime):
        totalTime = DIFS + self.backOff + FRAME + SIFS
        globalTime += totalTime
        return globalTime
