#!/usr/bin/python
import RPi.GPIO as GPIO
import PiShiftPy as shift
import time
import sys
import threading
import signal
from GrabGBMusic import BGMusic,Sound, BlastSound
from GrabGBLights import GrabGBLights
from GrabGBMattyWand import MattyWand
from GrabGBLogger import GrabLogger

Pack = {}

#############################
# user config
#############################
pin1 = 22			# serial power cell
pin2 = 17			# SRCLK
pin3 = 23			# RCLK
pin4 = 27			# serial cyclotron
pinMusic = 4			# enable disable music
pinWand = 25			# audio connection to wand
musicVolume = 1			# music volume
Pack['overheatSpeedThresh'] = 5	# seconds before speed up before overheat
Pack['overheatThresh'] = 10	# seconds before overheat
musicWhileOff = True		# allow music to run while power switch off
loggingEnabled = True		# whether to log to std out

soundFiles = {
	'start': "/opt/GB/Music/KJH_PackstartCombo.ogg", 		# pack turning on
	'hum': "/opt/GB/Music/protongun_amb_hum_loopLOUD.wav", 		# ambient sound always looping while pack on
	'stop': "/opt/GB/Music/KJH_PackstopDigital.ogg",		# pack turning off
	"scriptReady": "/opt/GB/Music/Mac.ogg", 			# when script is running and ready for commands
	"wandStart" : "/opt/GB/Music/WandShootStart.ogg", 		# start shooting sound
	"wandLoop": "/opt/GB/Music/WandShootLoop.ogg", 			# while shooting sound
	"wandEnd": "/opt/GB/Music/WandShootEnd.ogg", 			# stop shooting sound
	"beep": "/opt/GB/Music/protonpack_overheat_beep.wav",		# overheating beeping
	"vent": "/opt/GB/Music/protonpack_dry_vent.wav"			# venting sound after overheat
}

musicFiles = {
	'Higher': "/opt/GB/Music/HigherHigher.ogg",
	"Theme": "/opt/GB/Music/GBTheme.ogg",
	"WhichToPlay": "Theme"
}

#############################
# Let us know we are booted
#############################
ready = Sound(soundFiles["scriptReady"])
ready.play()

#############################
# Global and state vars
#############################
startSound = Sound(soundFiles["start"])									# start up sound
humSound = Sound(soundFiles["hum"], -1)									# bg sound of hum
Pack['Log'] = GrabLogger(loggingEnabled)								# write log files
Pack['blastSound'] = BlastSound(soundFiles["wandStart"], soundFiles["wandLoop"], soundFiles["wandEnd"])	# class for firing shooting
Pack['ventSound'] = Sound(soundFiles["vent"])								# overheating sounds
Pack['beepSound'] = Sound(soundFiles["beep"], 1)							# overheating sounds
music = BGMusic(musicVolume)										# music track
Pack['ggs'] = GrabGBLights(GrabLogger(loggingEnabled),pin1, pin2, pin3, pin4)				# powercell / cyclotron light class
Pack['isPlaying']= False										# music state
Pack['systemOn'] = False										# power switch state
Pack['isBlasting'] = False										# shooting state
Pack['blastTimer'] = time.time()									# how long blast button pressed
Pack['isOverheating'] = False										# overheat state
wandTracker = MattyWand()										# tracks commands from matty wand

#############################
# Async listener callbacks
#############################
# start and stop music
def MusicListener(channel):
	global Pack
	global musicWhileOff

	Pack['Log'].Log("Called music handler for " + musicFiles[musicFiles["WhichToPlay"]])
	if Pack['systemOn'] or musicWhileOff:
		if(Pack['isPlaying']):
			Pack['isPlaying'] = False
			music.stop()
		else:
			music.play()
			Pack['isPlaying'] = True

# listens for signals from wand
def WandListener(channel):
        global wandTracker
	global Pack

        if(wandTracker.initial == 0):
                threading.Timer(wandTracker.timeout, wandTracker.Process, ([Pack])).start()
                wandTracker.initial = 1
        wandTracker.Inc()

        Pack['Log'].Log("counter now: " + str(wandTracker.counter))

def quitHander(signum, frame):
	quitOut()
	exit()

# power off switch
def quitOut():
	global Pack
	global musicWhileOff
	if Pack['systemOn']:
		if not musicWhileOff:
			music.stop()
		Pack['systemOn'] = False
		humSound.stop()
		sound = Sound(soundFiles["stop"])
        	sound.play()
		Pack['ggs'].setMode("Empty")
		Pack['ggs'].processPattern()

#############################
# Main prog and loop
#############################

def main():
	# power on
	global Pack
	global musicFiles
	global pinMusic
	global pinWand
	global wandTracker

	music.setTrack(musicFiles[musicFiles["WhichToPlay"]])

	GPIO.setmode(GPIO.BCM)
	GPIO.setup(pinMusic, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)				# start and stop music
	GPIO.setup(pinWand, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)                                # wand connection

        GPIO.add_event_detect(pinMusic, GPIO.FALLING, callback=MusicListener, bouncetime=1000)	# start and stop music
	GPIO.add_event_detect(pinWand, GPIO.RISING, callback=WandListener)                      # wand connection

	signal.signal(signal.SIGINT, quitHander)						# catch control+c

	# main loop
	while True:
		# if switch on state
		if wandTracker.systemOn:							# uncomment to turn on with wand, comment to always on
		#if True:									# uncomment to boot on, comment to turn on with wand
			# we were off so start power up sequence
			if not Pack['systemOn']:
				startSound.play()
        			humSound.play()
				Pack['systemOn'] = True
				Pack['ggs'].setMode("Fill")
			# blink lights
			Pack['ggs'].processPattern()
		# switch is off
		else:
			# power down sequence
			quitOut()

if __name__ == "__main__":
	main()
