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
		# We check the home feed, mentions and DMs
		self.homeTimeLine = ''
		self.mentionsTimeLine = ''
		self.directMessagesTimeLine = ''

		# Interval to poll twitter
		self.updateInterval = updateInterval
		self.lastUpdate = 0

		# So we can request only new tweets next time
		self.lastHomeTimeLineID = 0
		self.lastMentionID = 0
		self.lastDirectMessageID = 0

		# Has the current update been "handled" by  the button being pressed?
		self.currentUpdateHandled = True

		self.update()

	# Methods for simple refreshing of various aspects of Twitter
	# Twitter rate limits for requests are easily exceeded, so we need exception handling
	# to deal with Twitter refusing us

	def refreshHomeTimeLine(self):
		try:
			if self.lastHomeTimeLineID:
				self.homeTimeLine = self.twitterClient.statuses.home_timeline(since_id = self.lastHomeTimeLineID)
			else:
				self.homeTimeLine = self.twitterClient.statuses.home_timeline()
		except urllib2.URLError, e:
			print 'Error getting homeTimeLine: ', e.errno
		except TwitterHTTPError, e:
			print 'TwitterError: ', e

		#print 'Most recent tweeter: ' + str(self.mostRecentTweeter())

		if self.homeTimeLine:
			self.lastHomeTimeLineID = self.homeTimeLine[0]['id']

		print 'Num tweets: ', len(self.homeTimeLine)

	def refreshMentions(self):
		try:
			if self.lastMentionID:
				self.mentionsTimeLine = self.twitterClient.statuses.mentions_timeline(since_id = self.lastMentionID)
			else:
				self.mentionsTimeLine = self.twitterClient.statuses.mentions_timeline()
		except urllib2.URLError, e:
			print 'Error getting mentionsTimeLine: ', e.errno
		except TwitterHTTPError, e:
			print 'TwitterError: ', e

		#print 'Most recent mention from: ', self.mostRecentMentioner()

		if self.mentionsTimeLine:
			self.lastMentionID = self.mentionsTimeLine[0]['id']

		print 'Num mentions: ', len(self.mentionsTimeLine)

	def refreshDirectMessages(self):
		try:
			if self.lastDirectMessageID:
				self.directMessagesTimeLine = self.twitterClient.direct_messages(since_id = self.lastDirectMessageID)
			else:
				self.directMessagesTimeLine = self.twitterClient.direct_messages()
		except urllib2.URLError, e:
			print 'Error getting directMessagesTimeLine: ', e.errno
		except TwitterHTTPError, e:
			print 'TwitterError: ', e

		#print 'Most recent direct message from: ' + str(self.mostRecentDirectMessager())
		#print 'Most recent direct message content: ' + str(self.mostRecentDirectMessageText())

		if self.directMessagesTimeLine:
			self.lastDirectMessageID = self.directMessagesTimeLine[0]['id']

		print 'Num direct messages: ', len(self.directMessagesTimeLine)
		

	# Some misc utility funcs
	# Note, these **only** deal with stuff in the most recent update

	def mostRecentTweeter(self):
		if self.homeTimeLine:
			return self.homeTimeLine[0]['user']['screen_name']
		else:
			return None

	def mostRecentMentioner(self):
		if self.mentionsTimeLine:
			return self.mentionsTimeLine[0]['user']['screen_name']
		else:
			return None

	def mostRecentDirectMessager(self):
		if self.directMessagesTimeLine:
			return self.directMessagesTimeLine[0]['sender']['screen_name']
		else:
			return None
		#print 'Most recent direct message content: ' + self.directMessagesTimeLine[0]['text']

	def mostRecentDirectMessageText(self):
		if self.directMessagesTimeLine:
			return self.directMessagesTimeLine[0]['text']
		else:
			return None

	# These look for the string within message or in its entirity
	# depending on the flag set

	def mentionWithString(self, strToMatch, subStr):
		for i in range(0, len(self.mentionsTimeLine)):
			if subStr:
				if strToMatch in self.homeTimeLine[i]['text'].lower():
					return self.homeTimeLine[i]['text']
			else:
				if self.mentionsTimeLine[i]['text'].lower() == strToMatch:
					return self.homeTimeLine[i]['text']
		return False

	def tweetWithString(self, strToMatch, subStr):
		for i in range(0, len(self.homeTimeLine)):
			if subStr:
				if strToMatch in self.homeTimeLine[i]['text'].lower():
					return self.homeTimeLine[i]['text']
			else:
				if self.homeTimeLine[i]['text'].lower() == strToMatch:
					return self.homeTimeLine[i]['text']
		return False

	def directMessageWithString(self, strToMatch, subStr):
		for i in range(0, len(self.directMessagesTimeLine)):
			if subStr:
				if strToMatch in self.homeTimeLine[i]['text'].lower():
					return self.homeTimeLine[i]['text']
			else:
				if self.directMessagesTimeLine[i]['text'].lower() == strToMatch:
					return self.homeTimeLine[i]['text']
		return False

	# Update handling (with interval checking)

	def update(self):
		if self.isReadyForUpdate():
			print 'TwitterReader update'
			self.refreshHomeTimeLine()
			self.refreshMentions()
			self.refreshDirectMessages()
			self.currentUpdateHandled = False
			print 'Update complete'

	def isReadyForUpdate(self):
		if time.mktime(time.gmtime()) - self.lastUpdate > self.updateInterval:
			self.lastUpdate = int(time.time())
			return True
		else:
			return False
