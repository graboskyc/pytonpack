#!/usr/bin/python
import RPi.GPIO as GPIO
from time import sleep

# Original Author: Shrikant Patnaik
# https://github.com/shrikantpatnaik/PiShiftPy
# modified by Chris Grabosky to create a class to allow multiple instances rather than relying on global vars
# further modified to dual write to two registers in parallel

class PSP:
	def __init__(self, data_pinA, clock_pin, latch_pin):
	    self.dataPC = data_pinA
	    self.clock = clock_pin
	    self.latch = latch_pin
	    self.setup()
	
	
	def setup(self):
	    GPIO.setwarnings(False)
	    GPIO.setmode(GPIO.BCM)
	    GPIO.setup(self.dataPC, GPIO.OUT)
	    GPIO.setup(self.clock, GPIO.OUT, initial=GPIO.LOW)
	    GPIO.setup(self.latch, GPIO.OUT, initial=GPIO.LOW)
	    self.write(0)
	
	
	def write_latch(self):
	    GPIO.output(self.latch, 1)
	    GPIO.output(self.latch, 0)
	
	
	def push_bit(self,bita):
	    GPIO.output(self.clock, 0)
	    GPIO.output(self.dataPC, bita)
	    GPIO.output(self.clock, 1)
	
	
	def get_bit(self, value, n):
	    if value & (1 << n):
	        return 1
	    else:
	        return 0
	
	
	def write(self, valuea):
	    for i in reversed(range(16)):
		self.push_bit(self.get_bit(valuea, i))

	    self.write_latch()
