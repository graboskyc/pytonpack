#!/usr/bin/python
import RPi.GPIO as GPIO
import PiShiftPy as shift
import time
import sys

class GrabGBShift:
	def __init__(self, pin1, pin2, pin3, srct):
		self.pin1 = pin1
		self.pin2 = pin2
		self.pin3 = pin3
		self.srct = srct
		self.setMode("Fill")
		self.pattern = []
		self.defaultBlinkDelay = .09
		self.blinkDelay = self.defaultBlinkDelay

		self.getPattern()
		shift.init(pin1,pin2,pin3,srct)
		self.shift = shift

	def adjustSpeed(self, delay):
		self.blinkDelay = delay

	def getMode(self):
		return self.mode

	def defaultSpeed(self):
		self.blinkDelay = self.defaultBlinkDelay

	def getPattern(self):
		mode = self.mode
		pattern = []
		#power on and off seq
		if (mode == "Fill") or (mode == "Empty"):
                	pattern.append(0x0000) # 00000000000000
			pattern.append(0x2000) # 10000000000000
			pattern.append(0x1000) # 01000000000000
			pattern.append(0x0800) # 00100000000000
			pattern.append(0x0400) # 00010000000000
			pattern.append(0x0200) # 00001000000000
			pattern.append(0x0100) # 00000100000000
			pattern.append(0x0080) # 00000010000000
			pattern.append(0x0040) # 00000001000000
			pattern.append(0x0020) # 00000000100000
			pattern.append(0x0010) # 00000000010000
			pattern.append(0x0008) # 00000000001000
			pattern.append(0x0004) # 00000000000100
			pattern.append(0x0002) # 00000000000010
			pattern.append(0x0001) # 00000000000001
			pattern.append(0x2001) # 10000000000001
			pattern.append(0x1001) # 01000000000001
			pattern.append(0x0801) # 00100000000001
			pattern.append(0x0801) # 00010000000001
			pattern.append(0x0201) # 00001000000001
			pattern.append(0x0101) # 00000100000001
			pattern.append(0x0081) # 00000010000001
			pattern.append(0x0041) # 00000001000001
			pattern.append(0x0021) # 00000000100001
			pattern.append(0x0011) # 00000000010001
			pattern.append(0x0009) # 00000000001001
			pattern.append(0x0005) # 00000000000101
			pattern.append(0x0003) # 00000000000011
			pattern.append(0x2003) # 10000000000011
			pattern.append(0x1003) # 01000000000011
			pattern.append(0x0803) # 00100000000011
			pattern.append(0x0403) # 00010000000011
			pattern.append(0x0203) # 00001000000011
			pattern.append(0x0103) # 00000100000011
			pattern.append(0x0083) # 00000010000011
			pattern.append(0x0043) # 00000001000011
			pattern.append(0x0023) # 00000000100011
			pattern.append(0x0013) # 00000000010011
			pattern.append(0x000B) # 00000000001011
			pattern.append(0x0007) # 00000000000111
			pattern.append(0x2007) # 10000000000111
			pattern.append(0x1007) # 01000000000111
			pattern.append(0x0807) # 00100000000111
			pattern.append(0x0407) # 00010000000111
			pattern.append(0x0207) # 00001000000111
			pattern.append(0x0107) # 00000100000111
			pattern.append(0x0087) # 00000010000111
			pattern.append(0x0047) # 00000001000111
			pattern.append(0x0027) # 00000000100111
			pattern.append(0x0017) # 00000000010111
			pattern.append(0x000F) # 00000000001111
			pattern.append(0x080F) # 00100000001111
			pattern.append(0x040F) # 00010000001111
			pattern.append(0x020F) # 00001000001111
			pattern.append(0x010F) # 00000100001111
			pattern.append(0x008F) # 00000010001111
			pattern.append(0x004F) # 00000001001111
			pattern.append(0x002F) # 00000000101111
			pattern.append(0x001F) # 00000000011111
			pattern.append(0x201F) # 10000000011111
			pattern.append(0x101F) # 01000000011111
			pattern.append(0x081F) # 00100000011111
			pattern.append(0x041F) # 00010000011111
			pattern.append(0x021F) # 00001000011111
			pattern.append(0x011F) # 00000100011111
			pattern.append(0x009F) # 00000010011111
			pattern.append(0x005F) # 00000001011111
			pattern.append(0x003F) # 00000000111111
			pattern.append(0x203F) # 10000000111111
			pattern.append(0x103F) # 01000000111111
			pattern.append(0x083F) # 00100000111111
			pattern.append(0x043F) # 00010000111111
			pattern.append(0x023F) # 00001000111111
			pattern.append(0x013F) # 00000100111111
			pattern.append(0x00BF) # 00000010111111
			pattern.append(0x007F) # 00000001111111
			pattern.append(0x207F) # 10000001111111
			pattern.append(0x107F) # 01000001111111
			pattern.append(0x087F) # 00100001111111
			pattern.append(0x047F) # 00010001111111
			pattern.append(0x027F) # 00001001111111
			pattern.append(0x017F) # 00000101111111
			pattern.append(0x00FF) # 00000011111111
			pattern.append(0x20FF) # 10000011111111
			pattern.append(0x10FF) # 01000011111111
			pattern.append(0x08FF) # 00100011111111
			pattern.append(0x04FF) # 00010011111111
			pattern.append(0x02FF) # 00001011111111
			pattern.append(0x01FF) # 00000111111111
			pattern.append(0x21FF) # 10000111111111
			pattern.append(0x11FF) # 01000111111111
			pattern.append(0x09FF) # 00100111111111
			pattern.append(0x05FF) # 00010111111111
			pattern.append(0x03FF) # 00001111111111
			pattern.append(0x23FF) # 10001111111111
			pattern.append(0x13FF) # 01001111111111
			pattern.append(0x0BFF) # 00101111111111
			pattern.append(0x07FF) # 00011111111111
			pattern.append(0x27FF) # 10011111111111
			pattern.append(0x17FF) # 01011111111111
			pattern.append(0x0FFF) # 00111111111111
			pattern.append(0x2FFF) # 10111111111111
			pattern.append(0x1FFF) # 01111111111111
			pattern.append(0x2FFF) # 11111111111111

		if (mode == "Proton") or (mode == "Slime"):
			pattern.append(0x0000) # 00000000000000
			pattern.append(0x0001) # 00000000000001
			pattern.append(0x0003) # 00000000000011
			pattern.append(0x0007) # 00000000000111
			pattern.append(0x000F) # 00000000001111
			pattern.append(0x001F) # 00000000011111
			pattern.append(0x003F) # 00000000111111
			pattern.append(0x007F) # 00000001111111
			pattern.append(0x00FF) # 00000011111111
			pattern.append(0x01FF) # 00000111111111
			pattern.append(0x03FF) # 00001111111111
			pattern.append(0x07FF) # 00011111111111
			pattern.append(0x0FFF) # 00111111111111
			pattern.append(0x1FFF) # 01111111111111
			pattern.append(0x3FFF) # 11111111111111
		if (mode == "Slime") or (mode == "Fill"):
			pattern.append(0x1FFF) # 01111111111111
			pattern.append(0x0FFF) # 10111111111111
			pattern.append(0x07FF) # 00011111111111
			pattern.append(0x03FF) # 00001111111111
			pattern.append(0x01FF) # 00000111111111
			pattern.append(0x00FF) # 00000011111111
			pattern.append(0x007F) # 00000001111111
			pattern.append(0x003F) # 00000000111111
			pattern.append(0x001F) # 00000000011111
			pattern.append(0x000F) # 00000000001111
			pattern.append(0x0007) # 00000000000111
			pattern.append(0x0003) # 00000000000011
			pattern.append(0x0001) # 00000000000001
		if (mode == "DotIn") or (mode == "DotOut"):
                	pattern.append(0x0000) # 00000000000000
			pattern.append(0x2001) # 10000000000001
			pattern.append(0x1002) # 01000000000010
			pattern.append(0x0804) # 00100000000100
			pattern.append(0x0408) # 00010000001000
			pattern.append(0x0210) # 00001000010000
			pattern.append(0x0120) # 00000100100000
			pattern.append(0x00C0) # 00000011000000
		if (mode == "LineIn") or (mode == "LineOut"):
                	pattern.append(0x0000) # 00000000000000
                        pattern.append(0x2001) # 10000000000001
                        pattern.append(0x3003) # 11000000000011
                        pattern.append(0x3807) # 11100000000111
                        pattern.append(0x3C0F) # 11110000001111
                        pattern.append(0x3E1F) # 11111000011111
                        pattern.append(0x3F3F) # 11111100111111
                        pattern.append(0x3FFF) # 11111111111111
		if mode == "Pong":
			pattern.append(0x0000) # 00000000000000
                        pattern.append(0x2000) # 10000000000000
                        pattern.append(0x1000) # 01000000000000
                        pattern.append(0x0800) # 00100000000000
                        pattern.append(0x0400) # 00010000000000
                        pattern.append(0x0200) # 00001000000000
                        pattern.append(0x0100) # 00000100000000
                        pattern.append(0x0080) # 00000010000000
                        pattern.append(0x0040) # 00000001000000
                        pattern.append(0x0020) # 00000000100000
                        pattern.append(0x0010) # 00000000010000
                        pattern.append(0x0008) # 00000000001000
                        pattern.append(0x0004) # 00000000000100
                        pattern.append(0x0002) # 00000000000010
                        pattern.append(0x0001) # 00000000000001
			pattern.append(0x0002) # 00000000000010
			pattern.append(0x0004) # 00000000000100
			pattern.append(0x0008) # 00000000001000
			pattern.append(0x0010) # 00000000010000
			pattern.append(0x0020) # 00000000100000
			pattern.append(0x0040) # 00000001000000
			pattern.append(0x0080) # 00000010000000
			pattern.append(0x0100) # 00000100000000
			pattern.append(0x0200) # 00001000000000
			pattern.append(0x0400) # 00010000000000
			pattern.append(0x0800) # 00100000000000
			pattern.append(0x1000) # 01000000000000
			pattern.append(0x2000) # 10000000000000
		if mode == "Error1":
			pattern.append(0x2AAA) # 10101010101010
			pattern.append(0x1555) # 01010101010101
			pattern.append(0x2AAA) # 10101010101010
                        pattern.append(0x1555) # 01010101010101
			pattern.append(0x2AAA) # 10101010101010
                        pattern.append(0x1555) # 01010101010101
			pattern.append(0x3333) # 11001100110011
			pattern.append(0x0CCC) # 00110011001100
			pattern.append(0x3333) # 11001100110011
                        pattern.append(0x0CCC) # 00110011001100
			pattern.append(0x3333) # 11001100110011
                        pattern.append(0x0CCC) # 00110011001100
			pattern.append(0x3C0F) # 11110000001111
			pattern.append(0x03F0) # 00001111110000
			pattern.append(0x3C0F) # 11110000001111
                        pattern.append(0x03F0) # 00001111110000
			pattern.append(0x3C0F) # 11110000001111
                        pattern.append(0x03F0) # 00001111110000
		if (mode == "DotOut") or (mode == "LineOut") or (mode == "Empty"):
			pattern = pattern[::-1] # reverse it

		self.pattern = pattern

	def advanceMode(self):
		currentMode = self.mode
		if currentMode == "Proton":
			mode = "Slime"
		elif currentMode == "Slime":
        	        mode = "DotIn"
		elif currentMode == "DotIn":
        	        mode = "LineIn"
		elif currentMode == "LineIn":
        	        mode = "DotOut"
		elif currentMode == "DotOut":
        	        mode = "LineOut"
		elif currentMode == "LineOut":
        	        mode = "Pong"
		elif currentMode == "Pong":
			mode = "Error1"
		else:
			mode = "Proton"
		self.setMode(mode)

	def setMode(self, mode):
		print "setting mode to: " + mode
		self.mode = mode
		self.getPattern()

	def processPattern(self):
		pattern = self.pattern
		# copy locally so we dont adjust in the middle of a cycle
		localBlinkDelay = self.blinkDelay
		for bits in self.pattern:
	        	self.shift.write(bits)
	        	if(self.mode=="Fill"):
				time.sleep(.04)
			elif(self.mode=="Empty"):
	        		time.sleep(.03)
			elif(self.mode=="Pong"):
				time.sleep(.07)
			elif(self.mode=="Error1"):
				time.sleep(.15)
	        	else:
	        		time.sleep(localBlinkDelay)
		if(self.mode=="Fill"):
			self.setMode("Proton")
