import RPi.GPIO as GPIO

class TwitterGPIO:

	def __init__(self, outChannel, inChannel, delegateObj):
		self.outChannel = outChannel
		self.inChannel = inChannel
		self.lastSwitchState = 0
		self.delegateObj = delegateObj

		GPIO.setmode(GPIO.BCM)
		GPIO.setup(outChannel, GPIO.OUT, initial=GPIO.LOW)
		GPIO.setup(inChannel, GPIO.IN)

	def update(self):
		currSwitchState = GPIO.input(self.inChannel)

		if self.lastSwitchState == 1 and currSwitchState == 0:
			self.delegateObj.switchPressed(self)

		self.lastSwitchState = currSwitchState

	def turnOn(self):
		GPIO.output(self.outChannel, GPIO.HIGH)

	def turnOff(self):
		GPIO.output(self.outChannel, GPIO.LOW)

	def isOn(self):
		return GPIO.input(self.outChannel)