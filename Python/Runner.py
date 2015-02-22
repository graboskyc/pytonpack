#!/usr/bin/python
import RPi.GPIO as GPIO
import PiShiftPy as shift
import time
import sys
import threading
import signal
from GrabGBMusic import BGMusic,Sound, BlastSound
from GrabGBShift import GrabGBShift

#############################
# user config
#############################
pin1 = 22		# serial in
pin2 = 17		# SRCLK
pin3 = 23		# RCLK
pinPower = 4		# power switch 
pinMusic = 25		# enable disable music
pinShoot = 24		# shoot
shiftCount = 2		# number of shift registers
musicVolume = .5	# music volume
overheatThresh = 5	# seconds before overheat
musicWhileOff = False	# allow music to run while power switch off
soundFiles = {'start': "/opt/GB/Music/KJH_PackstartCombo.ogg", 'hum': "/opt/GB/Music/HumShort.wav", 'stop': "/opt/GB/Music/KJH_PackstopDigital.ogg", "scriptReady": "/opt/GB/Music/Mac.ogg"}
musicFiles = {'Higher': "/opt/GB/Music/HigherHigher.ogg", "Theme": "/opt/GB/Music/GBTheme.ogg"}

#############################
# Let us know we are booted
#############################

ready = Sound(soundFiles["scriptReady"])
ready.play()

#############################
# Global and state vars
#############################

startSound = Sound(soundFiles["start"])		# start up sound
humSound = Sound(soundFiles["hum"], -1)		# bg sound of hum
blastSound = BlastSound()			# class for firing shooting
music = BGMusic(musicVolume)			# music track
ggs = GrabGBShift(pin1, pin2, pin3, shiftCount)	# light class
isPlaying = False				# music state
systemOn = False				# power switch state
isBlasting = False				# shooting state
blastTimer = time.time()			# how long blast button pressed
isOverheating = False				# overheat state

#############################
# Async listener callbacks
#############################
# change light pattern
def LightListener(channel):
	print "Called light handler"
	ggs.advanceMode()

# start and stop music
def MusicListener(channel):
        print "Called music handler"
	global isPlaying
	global systemOn
	global musicWhileOff
	if systemOn or musicWhileOff:
		if(isPlaying):
			isPlaying = False
			music.stop()
		else:
			music.play()
			isPlaying = True

# overheat routine 
def overheat():
	global blastSound
	global isOverheating
	global isBlasting
	global ggs
	global systemOn

	blastSound.end()
	isBlasting = False
	ggs.setMode("Error1")
	time.sleep(3)
	systemOn = False
	
# start and stop shooting
def ShootListener(channel):
	print "Called shoot handler"
	global isBlasting
	global systemOn
	global isOverheating
	global blastTimer
	global overheatThresh
	if(systemOn):
		if((not isBlasting) and (not isOverheating)):
			isBlasting = True
			blastTime = time.time()
			blastSound.start()
			while ((GPIO.input(24) ==1) and (not isOverheating)):
				time.sleep(.01)
				if((time.time() - blastTime) > overheatThresh):
					isOverheating = True
				if isOverheating:
					overheat()
			if(not isOverheating):
				blastSound.end()
				isBlasting = False
	isOverheating = False

# called when control c
def quitHander(signum, frame):
	quitOut()
	exit()

# power off switch
def quitOut():
	global systemOn
	global musicWhileOff
	if systemOn:
		if not musicWhileOff:
			music.stop()
		systemOn = False
		humSound.stop()
		sound = Sound(soundFiles["stop"])
        	sound.play()
		ggs.setMode("Empty")
		ggs.processPattern()

#############################
# Main prog and loop
#############################

def main():
	# power on
	global systemOn
	global musicFiles
	global pinMusic
	global pinPower
	global pinShoot

	music.setTrack(musicFiles["Higher"])

	GPIO.setmode(GPIO.BCM)
	GPIO.setup(pinPower, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)	# power switch
	GPIO.setup(pinMusic, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)	# start and stop music
	GPIO.setup(pinShoot, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)	# shoot button

        GPIO.add_event_detect(pinMusic, GPIO.FALLING, callback=MusicListener, bouncetime=500)	# start and stop music
	GPIO.add_event_detect(pinShoot, GPIO.RISING, callback=ShootListener, bouncetime=500)	# shoot button
	signal.signal(signal.SIGINT, quitHander)

	# main loop
	while True:
		# if switch on state
		if(GPIO.input(pinPower) ==1 ):
			# we were off so start power up sequence
			if not systemOn:
				startSound.play()
        			humSound.play()
				systemOn = True
				ggs.setMode("Fill")
			# blink lights
			ggs.processPattern()
		# switch is off
		else:
			# power down sequence
			quitOut()

if __name__ == "__main__":
	main()
