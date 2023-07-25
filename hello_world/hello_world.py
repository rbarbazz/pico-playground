"""
This script toggles the LED every second
"""

from time import sleep
from machine import Pin

led = Pin("LED", Pin.OUT)

while True:
    led.toggle()
    sleep(1)
