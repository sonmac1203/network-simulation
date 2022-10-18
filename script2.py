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


while (
    globalTime <= SIMULATIONTIME // SLOTTIME
    and stationA.getIndexVal() < seriesLen
    and stationC.getIndexVal() < seriesLen
):

    arrivalTimeA = stationA.getArrivals()[stationA.getIndexVal()]
    arrivalTimeC = stationC.getArrivals()[stationC.getIndexVal()]

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
        lower.recordASuccess()
        lower.resetCW()
        lower.freeBackOff()
        lower.jump()

        """Upper might also be able to transmit"""
        transmissionSpan = arrivalLower + DIFS + backOffLower + RTS + SIFS + CTS + SIFS + FRAME + SIFS + ACK
        if arrivalUpper >= transmissionSpan:
            """Upper transmits successfully"""
            upper.recordASuccess()
            upper.resetCW()
            upper.freeBackOff()
            upper.jump()
        else:
            globalTime = transmissionSpan
    else:
        if arrivalLower + DIFS + backOffLower > arrivalUpper + DIFS + backOffUpper:
            """Upper transmits successfully"""
            upper.recordASuccess()
            upper.resetCW()
            upper.freeBackOff()
            upper.jump()
            """Lower freezes counter"""
            lower.freezeBackOff()
            lower.setBackOff(arrivalLower + backOffLower - arrivalUpper - backOffUpper)

            # Since the counter freezes, we want to start transmit right after this round
            globalTime += DIFS + backOffUpper + RTS + SIFS + CTS + SIFS + FRAME + SIFS + ACK
        elif arrivalLower + DIFS + backOffLower < arrivalUpper + DIFS + backOffUpper:
            """Lower transmits successfully"""
            lower.recordASuccess()
            lower.resetCW()
            lower.freeBackOff()
            lower.jump()
            """Upper freezes counter"""
            upper.freezeBackOff()
            upper.setBackOff(arrivalUpper + backOffUpper - arrivalLower - backOffLower)
            # Since the counter freezes, we want to start transmit right after this round
            globalTime += DIFS + backOffLower + RTS + SIFS + CTS + SIFS + FRAME + SIFS + ACK
        else:
            """A collision happens"""
            collisions += 1
            lower.jump()
            lower.freeBackOff()
            lower.doubleCW()
            upper.jump()
            upper.freeBackOff()
            upper.doubleCW()

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
