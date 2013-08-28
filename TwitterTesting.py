import os

import signal
import sys
import datetime

import RPi.GPIO as GPIO
import TwitterReader
import TwitterGPIO

# Assume lower case...
STRING_TO_MATCH = 'i love lamp'

#------------------------------------------------------------------

# Handle script being manually broken
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


	# Update systems
	# Test condition and react accordingly if met
	def update(self):
		self.twitGPIO.update()
		self.twitReader.update()

		if not self.twitReader.currentUpdateHandled:
			if not self.twitGPIO.isOn():
				testConditionResult = self.testCondition()
				if testConditionResult:
					self.twitGPIO.turnOn()
					print 'Turning light on due to matching condition! (' + str(datetime.datetime.now().time()) + ')'

	# Delegate callback from the twitGPIO object
	def switchPressed(self, switchObj):
		print 'Switch has been pressed'
		self.twitReader.currentUpdateHandled = True
		self.twitGPIO.turnOff()

	# Test multiple timelines for a match
	def testCondition(self):
		tweet = self.twitReader.tweetWithString(STRING_TO_MATCH, True)
		if tweet:
			print 'Matched string (' +STRING_TO_MATCH+ ') to tweet: ', tweet
			return tweet

		mention = self.twitReader.mentionWithString(STRING_TO_MATCH, True)
		if mention:
			print 'Matched string (' +STRING_TO_MATCH+ ') to mention: ', mention
			return mention

		directMessage = self.twitReader.directMessageWithString(STRING_TO_MATCH, True)
		if directMessage:
			print 'Matched string (' +STRING_TO_MATCH+ ') to direct message: ', directMessage
			return directMessage
		
		return False

#------------------------------------------------------------------

if __name__ == "__main__":
	
	os.environ['http_proxy'] = ''

	twitSwitch = TwitterSwitch()
	while True:
		twitSwitch.update()