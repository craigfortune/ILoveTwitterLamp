# IMPORTANT
# You need to put your own values in TwitterDetails.py for this to work!
# Required variables:
# AUTH_TOKEN, OAUTH_SECRET, CONSUMER_KEY, CONSUMER_SECRET
import TwitterDetails

from twitter import *
import time
import urllib2

class TwitterReader:

	def __init__(self, updateInterval):
		self.twitterClient = Twitter(auth = OAuth(	TwitterDetails.OAUTH_TOKEN,
													TwitterDetails.OAUTH_SECRET,
													TwitterDetails.CONSUMER_KEY,
													TwitterDetails.CONSUMER_SECRET
													))
		self.homeTimeLine = ''
		self.mentionsTimeLine = ''
		self.directMessagesTimeLine = ''

		self.updateInterval = updateInterval
		self.lastUpdate = 0

		self.lastHomeTimeLineID = 0
		self.lastMentionID = 0
		self.lastDirectMessageID = 0

		self.currentUpdateHandled = True

		self.update()

	# Methods for simple refreshing of various aspects of Twitter

	def refreshHomeTimeLine(self):
		try:
			if self.lastHomeTimeLineID:
				self.homeTimeLine = self.twitterClient.statuses.home_timeline(since_id = self.lastHomeTimeLineID)
			else:
				self.homeTimeLine = self.twitterClient.statuses.home_timeline()
		except urllib2.URLError, e:
			print 'Error getting homeTimeLine: ' + str(e.errno)

		print 'Most recent tweeter: ' + str(self.mostRecentTweeter())

		if self.homeTimeLine:
			self.lastHomeTimeLineID = self.homeTimeLine[0]['id']

	def refreshMentions(self):
		try:
			if self.lastMentionID:
				self.mentionsTimeLine = self.twitterClient.statuses.mentions_timeline(since_id = self.lastMentionID)
			else:
				self.mentionsTimeLine = self.twitterClient.statuses.mentions_timeline()
		except urllib2.URLError, e:
			print 'Error getting mentionsTimeLine: ' + str(e.errno)

		print 'Most recent mention from: ' + str(self.mostRecentMentioner())

		if self.mentionsTimeLine:
			self.lastMentionID = self.mentionsTimeLine[0]['id']

	def refreshDirectMessages(self):
		try:
			if self.lastDirectMessageID:
				self.directMessagesTimeLine = self.twitterClient.direct_messages(since_id = self.lastDirectMessageID)
			else:
				self.directMessagesTimeLine = self.twitterClient.direct_messages()
		except urllib2.URLError, e:
			print 'Error getting directMessagesTimeLine: ' + str(e.errno)

		print 'Most recent direct message from: ' + str(self.mostRecentDirectMessager())
		print 'Most recent direct message content: ' + str(self.mostRecentDirectMessageText())

		if self.directMessagesTimeLine:
			self.lastDirectMessageID = self.directMessagesTimeLine[0]['id']
		

	# Some misc utility funcs
	# Note, these **only** deal with stuff in the most recent update

	def mostRecentTweeter(self):
		if self.homeTimeLine:
			return self.homeTimeLine[0]['user']['screen_name']
		else:
			return False

	def mostRecentMentioner(self):
		if self.mentionsTimeLine:
			return self.mentionsTimeLine[0]['user']['screen_name']
		else:
			return False

	def mostRecentDirectMessager(self):
		if self.directMessagesTimeLine:
			return self.directMessagesTimeLine[0]['sender']['screen_name']
		else:
			return False
		#print 'Most recent direct message content: ' + self.directMessagesTimeLine[0]['text']

	def mostRecentDirectMessageText(self):
		if self.directMessagesTimeLine:
			return self.directMessagesTimeLine[0]['text']
		else:
			return False

	# Update handling (with interval checking)

	def update(self):
		if self.isReadyForUpdate():
			print 'TwitterReader update'
			self.refreshHomeTimeLine()
			self.refreshMentions()
			self.refreshDirectMessages()
			self.currentUpdateHandled = False

	def isReadyForUpdate(self):
		if time.mktime(time.gmtime()) - self.lastUpdate > self.updateInterval:
			self.lastUpdate = int(time.time())
			return True
		else:
			return False
