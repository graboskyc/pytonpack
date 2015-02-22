#!/usr/bin/python
import time
import sys
import pygame as pg
import threading

class BGMusic:
	def __init__(self, volume=0.8):
		self.volume = volume
		freq = 44100     # audio CD quality
                bitsize = -16    # unsigned 16 bit
                channels = 2     # 1 is mono, 2 is stereo
                buffer = 2048    # number of samples
                pg.mixer.init(freq, bitsize, channels, buffer)
		pg.mixer.music.set_volume(volume)
		self.pg = pg

	def setTrack(self, file):
		self.file = file

	def play(self):
        	try:                                                           
                	pg.mixer.music.load(self.file)
                	print("Music file {} loaded!".format(self.file))      
        	except pg.error:                                               
                	print("File {} not found! ({})".format(self.file, pg.get_error()))
                	return
        	pg.mixer.music.play()
	def stop(self):
		pg.mixer.music.stop()

class Sound:
        def __init__(self, file, loops=0):
                self.file = file
		pg.init()
		self.snd = pg.mixer.Sound(file)
		self.pg = pg
		self.loops = loops
        def play(self):
                self.snd.play(self.loops)
	def stop(self):
		self.snd.stop()

class BlastSound:
	def __init__(self, start, loop, end):
		self.startFile = start
		self.loopFile = loop
		self.endFile = end
		pg.init()
		self.startSound = pg.mixer.Sound(self.startFile)
		self.loopSound = pg.mixer.Sound(self.loopFile)
		self.endSound = pg.mixer.Sound(self.endFile)
		self.pg = pg
	def start(self):
		self.startSound.play()
		time.sleep(.5)
		self.loopSound.play(-1)
	def end(self):
		self.loopSound.stop()
		self.endSound.play()
