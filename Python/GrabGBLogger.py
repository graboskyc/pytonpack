#!/usr/bin/python

class GrabLogger:
	def __init__(self, enabled):
	    self.Enabled = enabled
	
	
	def Log(self, msg):
		if (self.Enabled):
			print msg
