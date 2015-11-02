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

	def ForceTogglePower(self, P):
		P['Log'].Log("Forcing power toggle")
		self.systemOn = not self.systemOn

        def Process(self, P):
		global isBlasting
                P['Log'].Log("Processing...")

                if(self.counter >= 6):
                        P['Log'].Log("Turned on")
			self.systemOn = True
		elif (self.counter == 2):
                #elif((self.counter == 1) or (self.counter == 2)):
			self.Shoot(P)
                        P['Log'].Log("Shooting start")
		elif(self.counter == 5):
			self.PowerDown(P)
		elif(self.counter == 3):
                #elif((self.counter == 3) or (self.counter == 4)):
                        P['Log'].Log("Shooting end")
			self.UnShoot(P)
                self.Zero()

	def Shoot(self, P):
		P['Log'].Log("Called matty shoot ")
	        noteFlag = False
	        if(P['systemOn']):
	                if((not self.isBlasting) and (not self.isOverheating)):
				P['Log'].Log("shorten your stream, i dont want my face burned off")
	                        self.isBlasting = True
	                        self.blastTime = time.time()
	                        P['blastSound'].start()
				threading.Timer(P['overheatSpeedThresh'], self.Overheat, ([P])).start()
				threading.Timer(P['overheatThresh'], self.Overheat, ([P])).start()

	def Overheat(self, P):
		P['Log'].Log("overheat routine")
		if(self.isBlasting):
			if((time.time() - self.blastTime) > P['overheatSpeedThresh']):
				P['ggs'].adjustSpeed(.04)
				P['Log'].Log("You should slow down before I overheat...")
				P['beepSound'].play()
			if((time.time() - self.blastTime) > P['overheatThresh']):
				P['Log'].Log("Oh its bad...")
        			#P['blastSound'].end()
        			#P['isBlasting'] = False
				#self.isBlasting = False
        			P['ggs'].setMode("Error1")
				P['beepSound'].play()
        			time.sleep(3)
				P['ventSound'].play()
        			P['systemOn'] = False
				P['ggs'].defaultSpeed()
	def PowerDown(self, P):
		self.systemOn = False
			
	def UnShoot(self, P):
		P['Log'].Log("called matty unshoot")
		if(not self.isBlasting):
			self.PowerDown(P)
		else:
			if(not self.isOverheating):
				P['Log'].Log("ending shoot sounds")
				P['blastSound'].end()
				self.isBlasting = False
			P['ggs'].defaultSpeed()
		self.isOverheating = False
