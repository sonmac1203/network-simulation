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

# testA = [0, 1000, 2000]
# testC = [0, 1007, 3000]

# stationA.setArrivals(testA)
# stationC.setArrivals(testC)

print(stationA.getArrivals()[:10])
print(stationC.getArrivals()[:10])

while (
    globalTime <= SIMULATIONTIME // SLOTTIME
    and stationA.getIndexVal() < seriesLen
    and stationC.getIndexVal() < seriesLen
):

    arrivalTimeA = stationA.getArrivalTime()
    arrivalTimeC = stationC.getArrivalTime()

    globalTime = min(arrivalTimeA, arrivalTimeC)

    backOffA = stationA.generateBackOff()
    backOffC = stationC.generateBackOff()

    stationB.setPeriodOfRTSFromA(arrivalTimeA + DIFS + backOffA, arrivalTimeA + DIFS + backOffA + RTS)
    stationB.setPeriodOfRTSFromC(arrivalTimeC + DIFS + backOffC, arrivalTimeC + DIFS + backOffC + RTS)

    if stationB.hasRTSCollision():
        """Has a RTS Collision"""
        collisions += 1

        stationA.freeBackOff()
        stationA.doubleCW()
        stationA.jump()

        stationC.freeBackOff()
        stationC.doubleCW()
        stationC.jump()
    else:
        if arrivalTimeA + backOffA > arrivalTimeC + backOffC:
            lower = stationC
            upper = stationA
        else:
            lower = stationA
            upper = stationC

        # Declarations for lower and upper
        arrivalLower = lower.getArrivalTime()
        backOffLower = lower.getBackOff()
        arrivalUpper = upper.getArrivalTime()
        backOffUpper = upper.getBackOff()

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
            transmissionSpan = arrivalLower + DIFS + backOffLower + RTS + SIFS + CTS + SIFS + FRAME + SIFS + ACK

            # check on this again
            if arrivalUpper >= transmissionSpan:
                """Upper transmits successfully"""
                upper.recordASuccess()
                upper.resetCW()
                upper.freeBackOff()
                upper.jump()
            else:
                if arrivalLower + DIFS + backOffLower + RTS + SIFS + CTS >= arrivalUpper + DIFS:
                    """Upper freezes the backoff"""
                    upper.freezeBackOff()
                    diff = arrivalUpper + backOffUpper - (arrivalLower + backOffLower + RTS + SIFS + CTS)
                    upper.setBackOff(diff)
                    upper.setArrivalTime(transmissionSpan)
                else:
                    pass

    if stationB.hasRTSCollision() is not True:
        if arrivalTimeA + backOffA > arrivalTimeC + backOffC:
            stationC = lower
            stationA = upper
        else:
            stationA = lower
            stationC = upper

print("\nNumber at successes at station A: " + str(stationA.getSuccesses()) + "\n")
print("Number at successes at station C: " + str(stationC.getSuccesses()) + "\n")
print("Number of collisions: " + str(collisions) + "\n")
print("Actual simulation time: " + str(globalTime * SLOTTIME) + "\n")
