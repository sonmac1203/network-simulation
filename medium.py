import numpy as np
from station import Station
from constants import *


class Medium:
    def __init__(self):
        self.occupied = False
        self.periodOccupiedByA = []
        self.periodOccupiedByC = []
        self.stationADoesTransmit = False
        self.stationCDoesTransmit = False

    def setPeriodOccupiedByA(self, s, e):
        self.periodOccupiedByA = [s, e]

    def setPeriodOccupiedByC(self, s, e):
        self.periodOccupiedByC = [s, e]

    def hasACollision(self):
        if (self.stationADoesTransmit and not self.stationCDoesTransmit) or (
            self.stationCDoesTransmit and not self.stationADoesTransmit
        ):
            return False
        startA = self.periodOccupiedByA[0]
        endA = self.periodOccupiedByA[1]
        startC = self.periodOccupiedByC[0]
        endC = self.periodOccupiedByC[1]
        return startA <= endC and endA >= startC

    def recordsStationADoesTransmit(self):
        self.stationADoesTransmit = True

    def recordsStationCDoesTransmit(self):
        self.stationCDoesTransmit = True

    def clearTransmissionRecords(self):
        self.stationADoesTransmit = False
        self.stationCDoesTransmit = False
