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

    