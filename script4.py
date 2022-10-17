"""Hidden Terminal Problem with CSMA/CA with VCS"""

import numpy as np
from station import Station
from medium4 import Medium4
from constants import *

seriesLen = LAMBDAS[LAMBDAINDEX] * SIMULATIONTIME

stationA = Station()
stationC = Station()
stationB = Medium4()

lower = Station()
upper = Station()

globalTime = 0
collisions = 0

testA = [0, 1000, 2000]
testC = [0, 1007, 3000]

# print(stationA.getArrivals()[:10])
# print("\n")
# print(stationC.getArrivals()[:10])

while globalTime <= SIMULATIONTIME // SLOTTIME and stationA.getIndex() < seriesLen and stationC.getIndex() < seriesLen:

    arrivalTimeA = stationA.getArrivals()[stationA.getIndex()]
    arrivalTimeC = stationC.getArrivals()[stationC.getIndex()]

    # arrivalTimeA = testA[stationA.getIndex()]
    # arrivalTimeC = testC[stationC.getIndex()]

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

    backOffLower = lower.getBackOff()
    backOffUpper = upper.getBackOff()

    stationB.setPeriodOfRTSFromLower(arrivalLower + DIFS + backOffLower, arrivalLower + DIFS + backOffLower + RTS)
    stationB.setPeriodOfRTSFromUpper(arrivalUpper + DIFS + backOffUpper, arrivalUpper + DIFS + backOffUpper + RTS)

    if stationB.hasRTSCollision():
        """Has a RTS Collision"""
        collisions += 1
        lower.jump()
        lower.freeBackOff()
        lower.doubleCW()
        upper.jump()
        upper.freeBackOff()
        upper.doubleCW()
    else:
        if arrivalLower + backOffLower > arrivalUpper + backOffUpper:  # swap in case lower goes ahead
            lower, upper = upper, lower
        """Lower transmits successfully"""
        lower.recordASuccess()
        lower.jump()
        lower.resetCW()
        lower.freeBackOff()
        if (
            arrivalLower + DIFS + backOffLower + RTS
            <= arrivalUpper + DIFS + backOffUpper
            <= arrivalLower + DIFS + backOffLower + RTS + SIFS + CTS
        ):
            """RTS from Upper is not received"""
            upper.doubleCW()
            upper.freeBackOff()
            upper.jump()
            collisions += 1
        else:
            # if and else here
            transmissionSpan = arrivalLower + DIFS + backOffLower + RTS + SIFS + CTS + SIFS + FRAME + SIFS + ACK
            if arrivalUpper + DIFS + backOffUpper >= transmissionSpan:
                """Upper transmits successfully"""
                upper.recordASuccess()
                upper.resetCW()
                upper.freeBackOff()
                upper.jump()
            else:
                # still error here
                if arrivalLower + DIFS + backOffLower + RTS + SIFS + CTS >= arrivalUpper + DIFS:
                    """Upper freezes the backoff"""
                    upper.freezeBackOff()
                    diff = arrivalUpper + backOffUpper - (arrivalLower + backOffLower + RTS + SIFS + CTS)
                    upper.setBackOff(diff)
                else:
                    pass

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
