import os

import signal
import sys
import datetime

import RPi.GPIO as GPIO
import TwitterReader
import TwitterGPIO

STRING_TO_MATCH = 'I love lamp'

#------------------------------------------------------------------

def signal_handler(signal, frame):
	print 'You pressed ctrl+c'
	print 'Cleaning up...'
	GPIO.cleanup()
	print 'Exiting...'
	sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

#------------------------------------------------------------------

class TwitterSwitch:

	def __init__(self):
		self.twitGPIO = TwitterGPIO.TwitterGPIO(18, 17, self)
		self.twitReader = TwitterReader.TwitterReader(65)


	def update(self):
		self.twitGPIO.update()
		self.twitReader.update()

		if not self.twitReader.currentUpdateHandled:
			if self.testCondition():
				if not self.twitGPIO.isOn():
					self.twitGPIO.turnOn()
					print 'Turning light on due to matching condition! (' + str(datetime.datetime.now().time()) + ')'

	def switchPressed(self, switchObj):
		print 'Switch has been pressed'
		self.twitReader.currentUpdateHandled = True
		self.twitGPIO.turnOff()

	def testCondition(self):
		if self.twitReader.mostRecentDirectMessageText() == STRING_TO_MATCH :
			return True
		else:
			return False


#------------------------------------------------------------------

if __name__ == "__main__":
	
	os.environ['http_proxy'] = ''

	twitSwitch = TwitterSwitch()
	while True:
		twitSwitch.update()