"""
microMPG backend driver for a terrible ADC running on an Arduino Nano.
"""

from . import Backend

import serial

class ADCBackend(Backend):
    def __init__(self) -> None:
        self.ser = serial.Serial('COM7', 256000, timeout=1)

    def read(self) -> List[int|float]:
        return 
