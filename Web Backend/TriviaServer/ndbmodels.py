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
#	Owners Class
#
class Owner(ndb.Model):
	userId = ndb.StringProperty()

#
#	Admin Class
#
class Admin(ndb.Model):
	userId = ndb.StringProperty()