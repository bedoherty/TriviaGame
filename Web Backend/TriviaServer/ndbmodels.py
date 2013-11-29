from google.appengine.ext import ndb

#
#	NDB Models
#
#	This class contains the NDB models for my TriviaGame project.
#
#	Author: Brian Doherty
#

#
#	Category Class
#
#class Category(ndb.Model):

#
#	Question Class
#
#class Question(ndb.Model):

#
#	User Properties Class
#
class UserProperty(ndb.Model):
	userName = ndb.StringProperty()
	userId = ndb.StringProperty()
	userStatus = ndb.StringProperty()

#
#	User Access Request Class
#
class AccessRequest(ndb.Model):
	userName = ndb.StringProperty()
	userId = ndb.StringProperty()
	requestedAccess = ndb.StringProperty()
	requestReason = ndb.StringProperty()