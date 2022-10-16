"""Hidden Terminal Problem with CSMA/CA"""

import numpy as np
from station import Station
from medium import Medium
from constants import *

lambdaIndex = 0
seriesLen = LAMBDAS[lambdaIndex] * SIMULATIONTIME

stationA = Station()
stationC = Station()
stationB = Medium()

globalTimeA = 0
globalTimeC = 0
collisions = 0

while globalTimeA <= SIMULATIONTIME // SLOTTIME or globalTimeC <= SIMULATIONTIME // SLOTTIME:

    packetArrivesFromA = stationA.getIndex() < seriesLen
    packetArrivesFromC = stationC.getIndex() < seriesLen

    # If a packet from A arrives
    if packetArrivesFromA:
        globalTimeA = stationA.getArrivals()[stationA.getIndex()]
        if globalTimeA <= SIMULATIONTIME // SLOTTIME:  # If still within simulation time
            backOffA = stationA.getBackOff()
            stationB.recordsStationADoesTransmit()
            stationB.setPeriodOccupiedByA(globalTimeA + DIFS + backOffA, globalTimeA + DIFS + backOffA + FRAME)

    # If a packet from C arrives
    if packetArrivesFromC:
        globalTimeC = stationC.getArrivals()[stationC.getIndex()]
        if globalTimeC <= SIMULATIONTIME // SLOTTIME:  # If still within simulation time
            backOffC = stationC.getBackOff()
            stationB.recordsStationCDoesTransmit()
            stationB.setPeriodOccupiedByC(globalTimeC + DIFS + backOffC, globalTimeC + DIFS + backOffC + FRAME)

    # If there is a collision
    if stationB.hasACollision():
        stationA.doubleCW()
        stationC.doubleCW()
        collisions += 1
    else:
        if packetArrivesFromA and globalTimeA <= SIMULATIONTIME // SLOTTIME:
            stationA.recordASuccess()
            stationA.resetCW()
        if packetArrivesFromC and globalTimeC <= SIMULATIONTIME // SLOTTIME:
            stationC.recordASuccess()
            stationC.resetCW()

    stationA.jump()
    stationC.jump()
    stationB.clearTransmissionRecords()

print("\nNumber at successes at station A: " + str(stationA.getSuccesses()) + "\n")
print("Number at successes at station C: " + str(stationC.getSuccesses()) + "\n")
print("Number of collisions: " + str(collisions) + "\n")
print("Actual simulation time of A: " + str(globalTimeA * SLOTTIME) + "\n")
print("Actual simulation time of C: " + str(globalTimeC * SLOTTIME) + "\n")
