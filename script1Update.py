import numpy as np
from station import Station
from constants import *

seriesLen = LAMBDAS[LAMBDAINDEX] * SIMULATIONTIME

stationA = Station()
stationC = Station()

lower = Station()
upper = Station()

globalTime = 0
collisions = 0

# print(stationA.getArrivals()[:10])
# print(stationC.getArrivals()[:10])

testA = [20, 1000, 2000]
testC = [23, 1007, 3000]


def transmitJob(station: Station):
    station.recordASuccess()
    station.resetCW()
    station.freeBackOff()
    station.jump()


def collisionJob(station: Station):
    station.doubleCW()
    station.freeBackOff()
    station.jump()


while (
    globalTime <= SIMULATIONTIME // SLOTTIME
    and stationA.getIndexVal() < seriesLen
    and stationC.getIndexVal() < seriesLen
):

    arrivalTimeA = stationA.getArrivals()[stationA.getIndexVal()]
    arrivalTimeC = stationC.getArrivals()[stationC.getIndexVal()]

    # arrivalTimeA = testA[stationA.getIndexVal()]
    # arrivalTimeC = testC[stationC.getIndexVal()]

    if arrivalTimeA <= arrivalTimeC:
        lower = stationA
        upper = stationC
    else:
        lower = stationC
        upper = stationA

    arrivalLower = min(arrivalTimeA, arrivalTimeC)
    arrivalUpper = max(arrivalTimeA, arrivalTimeC)

    if globalTime >= min(arrivalLower, arrivalUpper):
        arrivalLower = globalTime
    elif globalTime < min(arrivalLower, arrivalUpper):
        globalTime = arrivalLower

    backOffLower = lower.generateBackOff()
    backOffUpper = upper.generateBackOff()

    if arrivalLower + DIFS + backOffLower < arrivalUpper + DIFS:
        """Lower transmits successfully"""
        transmitJob(lower)
        """Upper might also be able to transmit"""
        transmissionSpan = arrivalLower + DIFS + backOffLower + FRAME + SIFS + ACK
        if arrivalUpper >= transmissionSpan:
            """Upper transmits successfully"""
            transmitJob(upper)
        else:
            globalTime = transmissionSpan
    else:
        if arrivalLower + DIFS + backOffLower > arrivalUpper + DIFS + backOffUpper:
            """Upper transmits successfully"""
            transmitJob(upper)
            """Lower freezes counter"""
            lower.freezeBackOff()
            lower.setBackOff(arrivalLower + backOffLower - arrivalUpper - backOffUpper)
            # Since the counter freezes, we want to start transmit right after this round
            globalTime += DIFS + backOffUpper + FRAME + SIFS + ACK
        elif arrivalLower + DIFS + backOffLower < arrivalUpper + DIFS + backOffUpper:
            """Lower transmits successfully"""
            transmitJob(lower)
            """Upper freezes counter"""
            upper.freezeBackOff()
            upper.setBackOff(arrivalUpper + backOffUpper - arrivalLower - backOffLower)
            # Since the counter freezes, we want to start transmit right after this round
            globalTime += DIFS + backOffLower + FRAME + SIFS + ACK
        else:
            """A collision happens"""
            collisions += 1
            collisionJob(lower)
            collisionJob(upper)

    # Assign back to A and C
    if arrivalTimeA <= arrivalTimeC:
        stationA = lower
        stationC = upper
    else:
        stationC = lower
        stationA = upper

print("\nNumber at successes at station A: " + str(stationA.getSuccesses()) + "\n")
print("Number at successes at station C: " + str(stationC.getSuccesses()) + "\n")
print("Number of collisions: " + str(collisions) + "\n")
print("Actual simulation time: " + str(globalTime * SLOTTIME) + "\n")
