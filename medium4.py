import numpy as np
from station import Station
from constants import *


class Medium4:
    # def __init__(self):
    #     self.occupied = False
    #     self.periodOccupiedByA = []
    #     self.periodOccupiedByC = []
    #     self.stationADoesTransmit = False
    #     self.stationCDoesTransmit = False

    # def setPeriodOccupiedByA(self, s, e):
    #     self.periodOccupiedByA = [s, e]

    # def setPeriodOccupiedByC(self, s, e):
    #     self.periodOccupiedByC = [s, e]

    # def hasACollision(self):
    #     if (self.stationADoesTransmit and not self.stationCDoesTransmit) or (
    #         self.stationCDoesTransmit and not self.stationADoesTransmit
    #     ):
    #         return False
    #     startA = self.periodOccupiedByA[0]
    #     endA = self.periodOccupiedByA[1]
    #     startC = self.periodOccupiedByC[0]
    #     endC = self.periodOccupiedByC[1]
    #     return startA <= endC and endA >= startC

    # def recordsStationADoesTransmit(self):
    #     self.stationADoesTransmit = True

    # def recordsStationCDoesTransmit(self):
    #     self.stationCDoesTransmit = True

    # def clearTransmissionRecords(self):
    #     self.stationADoesTransmit = False
    #     self.stationCDoesTransmit = False

    def __init__(self):
        self.sendingCTS = False
        self.periodOfRTSFromLower = []
        self.periodOfRTSFromUpper = []
        self.periodOfRTSFromA = []
        self.periodOfRTSFromC = []

    def setPeriodOfRTSFromLower(self, s, e):
        self.periodOfRTSFromLower = [s, e]

    def setPeriodOfRTSFromUpper(self, s, e):
        self.periodOfRTSFromUpper = [s, e]

    def setPeriodOfRTSFromA(self, s, e):
        self.periodOfRTSFromA = [s, e]

    def setPeriodOfRTSFromC(self, s, e):
        self.periodOfRTSFromC = [s, e]

    def hasRTSCollision(self):
        startL = self.periodOfRTSFromA[0]
        endL = self.periodOfRTSFromA[1]
        startU = self.periodOfRTSFromC[0]
        endU = self.periodOfRTSFromC[1]
        return startL < endU and endL > startU
