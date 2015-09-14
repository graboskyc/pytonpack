#!/usr/bin/python
import time
import threading

class MattyWand:
        def __init__(self):
                self.Zero()
		self.systemOn = False
		self.isBlasting = False
		self.blastTime = ''
		self.isOverheating = False
        def Zero(self):
                self.initial = 0
                self.last = 0
                self.timeout =.1 
                self.counter = 0

        def Inc(self):
                self.counter = self.counter + 1

        def Process(self, P):
		global isBlasting
                print "Processing..."

                if(self.counter >= 6):
                        print "Turned on"
			self.systemOn = True
                elif((self.counter == 1) or (self.counter == 2)):
			self.Shoot(P)
                        print "Shooting start"
                elif((self.counter == 3) or (self.counter == 4)):
                        print "Shooting end"
			self.UnShoot(P)
                self.Zero()

	def Shoot(self, P):
		print "Called matty shoot "
	        noteFlag = False
	        if(P['systemOn']):
	                if((not self.isBlasting) and (not self.isOverheating)):
				print "shorten your stream, i dont want my face burned off"
	                        self.isBlasting = True
	                        self.blastTime = time.time()
	                        P['blastSound'].start()
				threading.Timer(P['overheatSpeedThresh'], self.Overheat, ([P])).start()
				threading.Timer(P['overheatThresh'], self.Overheat, ([P])).start()

	def Overheat(self, P):
		print "overheat routine"
		if(self.isBlasting):
			if((time.time() - self.blastTime) > P['overheatSpeedThresh']):
				P['ggs'].adjustSpeed(.04)
				print "You should slow down before I overheat..."
				P['beepSound'].play()
			if((time.time() - self.blastTime) > P['overheatThresh']):
				print "Oh its bad..."
        			#P['blastSound'].end()
        			#P['isBlasting'] = False
				#self.isBlasting = False
        			P['ggs'].setMode("Error1")
				P['beepSound'].play()
        			time.sleep(3)
				P['ventSound'].play()
        			P['systemOn'] = False
				P['ggs'].defaultSpeed()
			
	def UnShoot(self, P):
		print "called matty unshoot"
		if(not self.isBlasting):
                        print "turn me off"
			self.systemOn = False
		else:
			if(not self.isOverheating):
				print "ending shoot sounds"
				P['blastSound'].end()
				self.isBlasting = False
			P['ggs'].defaultSpeed()
		self.isOverheating = False
