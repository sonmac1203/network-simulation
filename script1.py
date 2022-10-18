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


def transmitJob(station: Station):
    station.recordASuccess()
    station.jump()
    station.resetCW()


def transmitJobWithFreezingBackoff(station1: Station, station2: Station, arrival1, backoff1, arrival2, backoff2):
    transmitJob(station1)
    station2.freezeBackOff()
    diff = arrival2 + backoff2 - arrival1 - backoff1
    station2.setBackOff(diff)


while (
    globalTime <= SIMULATIONTIME // SLOTTIME
    and stationA.getIndexVal() < seriesLen
    and stationC.getIndexVal() < seriesLen
):
    arrivalA = stationA.getArrivals()[stationA.getIndexVal()]
    arrivalC = stationC.getArrivals()[stationC.getIndexVal()]

    if arrivalA <= arrivalC:
        lower = stationA
        upper = stationC
    else:
        lower = stationC
        upper = stationA

    arrivalLower = lower.getArrivals()[lower.getIndexVal()]
    arrivalUpper = upper.getArrivals()[upper.getIndexVal()]

    if globalTime >= min(arrivalLower, arrivalUpper):
        arrivalLower = globalTime
    elif globalTime < min(arrivalLower, arrivalUpper):
        globalTime = arrivalLower

    if arrivalLower + DIFS <= arrivalUpper:
        backOffLower = lower.generateBackOff()
        if arrivalLower + DIFS + backOffLower <= arrivalUpper:
            """Lower transmits"""
            globalTime = lower.transmit(globalTime)
            transmitJob(lower)
        else:
            if arrivalLower + DIFS + backOffLower < arrivalUpper + DIFS:
                """Lower transmits"""
                transmitJob(lower)
            else:  # Starting here we need to account for backoff freezing
                backOffUpper = upper.generateBackOff()
                if arrivalLower + DIFS + backOffLower < arrivalUpper + DIFS + backOffUpper:
                    """Lower transmits"""
                    globalTime = lower.transmit(globalTime)
                    transmitJobWithFreezingBackoff(lower, upper, arrivalLower, backOffLower, arrivalUpper, backOffUpper)
                elif arrivalLower + DIFS + backOffLower > arrivalUpper + DIFS + backOffUpper:
                    """Upper transmits"""
                    globalTime = upper.transmit(globalTime)
                    transmitJobWithFreezingBackoff(upper, lower, arrivalUpper, backOffUpper, arrivalLower, backOffLower)
                else:
                    """A collision happens"""
                    lower.doubleCW()
                    lower.jump()
                    upper.doubleCW()
                    upper.jump()
                    globalTime = lower.collide(globalTime)
                    collisions += 1

    else:
        backOffLower = lower.generateBackOff()
        if arrivalLower + DIFS + backOffLower <= arrivalUpper + DIFS:
            """Lower transmits"""
            globalTime = lower.transmit(globalTime)
            transmitJob(lower)
        else:  # Starting here we need to account for backoff freezing
            backOffUpper = upper.generateBackOff()
            if arrivalLower + DIFS + backOffLower < arrivalUpper + DIFS + backOffUpper:
                """Lower transmits"""
                globalTime = lower.transmit(globalTime)
                transmitJobWithFreezingBackoff(lower, upper, arrivalLower, backOffLower, arrivalUpper, backOffUpper)
            elif arrivalLower + DIFS + backOffLower > arrivalUpper + DIFS + backOffUpper:
                """Upper transmits"""
                globalTime = upper.transmit(globalTime)
                transmitJobWithFreezingBackoff(upper, lower, arrivalUpper, backOffUpper, arrivalLower, backOffLower)
            else:
                """A collision happens"""
                lower.doubleCW()
                lower.jump()
                upper.doubleCW()
                upper.jump()
                globalTime = lower.collide(globalTime)
                collisions += 1

    # Assign back to A and C
    if arrivalA <= arrivalC:
        stationA = lower
        stationC = upper
    else:
        stationC = lower
        stationA = upper

print("\nNumber at successes at station A: " + str(stationA.getSuccesses()) + "\n")
print("Number at successes at station C: " + str(stationC.getSuccesses()) + "\n")
print("Number of collisions: " + str(collisions) + "\n")
print("Actual simulation time: " + str(globalTime * SLOTTIME) + "\n")
