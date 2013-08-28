import RPi.GPIO as GPIO

class TwitterGPIO:

	def __init__(self, outChannel, inChannel, delegateObj):
		self.outChannel = outChannel
		self.inChannel = inChannel
		self.lastSwitchState = 0
		self.delegateObj = delegateObj

		# Simple setup
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(outChannel, GPIO.OUT, initial=GPIO.LOW)
		GPIO.setup(inChannel, GPIO.IN)

	# Check switch state and fire off a delegate call if
	# a button press is completed (i.e. on the UP click)
	def update(self):
		currSwitchState = GPIO.input(self.inChannel)

		if self.lastSwitchState == 1 and currSwitchState == 0:
			if self.delegateObj:
				self.delegateObj.switchPressed(self)

		self.lastSwitchState = currSwitchState

	# Turning the output on/off etc
	def turnOn(self):
		GPIO.output(self.outChannel, GPIO.HIGH)

	def turnOff(self):
		GPIO.output(self.outChannel, GPIO.LOW)

	def isOn(self):
		return GPIO.input(self.outChannel)