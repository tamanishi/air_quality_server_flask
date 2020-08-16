#!/usr/bin/env python

import os
import sys
import datetime
from logging import basicConfig, getLogger, DEBUG, FileHandler, Formatter
from time import sleep

from ccs811 import CCS811

class AirQualityMonitor:
    CO2_PPM_THRESHOLD_1 = 1000
    CO2_PPM_THRESHOLD_2 = 2000

    CO2_LOWER_LIMIT  =  400
    CO2_HIGHER_LIMIT = 8192

    CO2_STATUS_CONDITIONING = 'CONDITIONING'
    CO2_STATUS_LOW          = 'LOW'
    CO2_STATUS_HIGH         = 'HIGH'
    CO2_STATUS_TOO_HIGH     = 'TOO HIGH'
    CO2_STATUS_ERROR        = 'ERROR'

    def __init__(self):
        self._ccs811 = CCS811()
        self.co2_status = self.CO2_STATUS_LOW

    def status(self, co2):
        if co2 < self.CO2_LOWER_LIMIT or co2 > self.CO2_HIGHER_LIMIT:
            return self.CO2_STATUS_CONDITIONING
        elif co2 < self.CO2_PPM_THRESHOLD_1:
            return self.CO2_STATUS_LOW
        elif co2 < self.CO2_PPM_THRESHOLD_2:
            return self.CO2_STATUS_HIGH
        else:
            return self.CO2_STATUS_TOO_HIGH

    def measure(self):
        while not self._ccs811.available():
            pass

        if not self._ccs811.available():
            # print("Currently not available...")
            return None

        try:
            if not self._ccs811.readData():
                co2 = self._ccs811.geteCO2()
                co2_status = self.status(co2)
                if co2_status == self.CO2_STATUS_CONDITIONING:
                    # print("Under Conditioning...")
                    return None

                # print("CO2: {0}ppm, TVOC: {1}".format(co2, self._ccs811.getTVOC()))

                air_quality = {
                    'timestamp' : datetime.datetime.now().isoformat(),
                    'co2' : co2,
                    'tvoc' : self._ccs811.getTVOC(),
                }
                return air_quality

            else:
                return None
        except:
            return None
