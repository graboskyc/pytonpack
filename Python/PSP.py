#!/usr/bin/python
import RPi.GPIO as GPIO
from time import sleep

# Original Author: Shrikant Patnaik
# https://github.com/shrikantpatnaik/PiShiftPy
# modified by Chris Grabosky to create a class to allow multiple instances rather than relying on global vars

class PSP:
	data = 18
	clock = 23
	latch = 24
	chain = 2

	def __init__(self, data_pin=18, clock_pin=23, latch_pin=24, chain_number=1):
	    self.data = data_pin
	    self.clock = clock_pin
	    self.latch = latch_pin
	    self.chain = chain_number
	    self.setup()
	
	
	def setup(self):
	    GPIO.setwarnings(False)
	    GPIO.setmode(GPIO.BCM)
	    GPIO.setup(self.data, GPIO.OUT)
	    GPIO.setup(self.clock, GPIO.OUT, initial=GPIO.LOW)
	    GPIO.setup(self.latch, GPIO.OUT, initial=GPIO.LOW)
	    self.write_all(0)
	
	
	def write_latch(self):
	    GPIO.output(self.latch, 1)
	    GPIO.output(self.latch, 0)
	
	
	def push_bit(self,bit):
	    GPIO.output(self.clock, 0)
	    GPIO.output(self.data, bit)
	    GPIO.output(self.clock, 1)
	
	
	def write_all(self,val):
	    for i in range(8*self.chain):
	        self.push_bit(val)
	    self.write_latch()
	
	
	def get_bit(self, value, n):
	    if value & (1 << n):
	        return 1
	    else:
	        return 0
	
	
	def write(self, value, shouldLatch = True):
	    if value.bit_length() > (8*self.chain):
	        raise ValueError("Tried to write more bits than available")
	    for i in reversed(range(8*self.chain)):
	        self.push_bit(self.get_bit(value, i))

            if shouldLatch:
	        self.write_latch()
	
	
	def test_pins(self):
	    for i in range(8*self.chain):
	        write(pow(2, i))
	        sleep(.125)
