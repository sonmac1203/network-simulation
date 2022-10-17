import numpy as np
from station import Station
from constants import *

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

while globalTime <= SIMULATIONTIME // SLOTTIME:
    arrivalA = stationA.getArrivals()[stationA.getIndex()]
    arrivalC = stationC.getArrivals()[stationC.getIndex()]

    backOffA = stationA.getBackOff()
    backOffC = stationC.getBackOff()

    timeA = arrivalA + DIFS + backOffA
    timeC = arrivalC + DIFS + backOffC

    if timeA + globalTime < timeC:
        """A finsihes before C"""
        globalTime = stationA.transmit(globalTime)
        transmitJob(stationA)
        stationC.doubleCW()
        stationC.jump()
    elif timeC + globalTime < timeA:
        """C finshes before A"""
        globalTime = stationC.transmit(globalTime)
        transmitJob(stationC)
        stationA.doubleCW()
        stationA.jump()
    else:
        """A collision happens"""
        globalTime = stationA.transmit(globalTime)
        stationA.doubleCW()
        stationA.jump()
        stationC.doubleCW()
        stationC.jump()
        collisions += 1

print("\nNumber at successes at station A: " + str(stationA.getSuccesses()) + "\n")
print("Number at successes at station C: " + str(stationC.getSuccesses()) + "\n")
print("Number of collisions: " + str(collisions) + "\n")
print("Actual simulation time: " + str(globalTime * SLOTTIME) + "\n")
