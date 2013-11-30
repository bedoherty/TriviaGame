#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
from ndbmodels import *
from google.appengine.ext import ndb
from google.appengine.api import users
import jinja2
import os
import urllib

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainHandler(webapp2.RequestHandler):
	def get(self):
		currUser = users.get_current_user()
		if currUser == None:
			self.redirect(users.create_login_url(self.request.uri))
		else:
			result = UserProperty.query(UserProperty.userId == currUser.user_id()).get()
			if result == None:
				self.response.write('Average Joe!')
				userProp = UserProperty(userId=currUser.user_id(), userName=currUser.nickname(), userStatus="Owner")
				userProp.put()
			else:
				template_values = {
					'name': currUser.nickname(),
				}
				template = JINJA_ENVIRONMENT.get_template('index_template.html')
				self.response.write(template.render(template_values))

class UsersPageHandler(webapp2.RequestHandler):
	def get(self):
		currUser = users.get_current_user()
		if currUser == None:
			self.redirect(users.create_login_url(self.request.uri))
		else:
			result = UserProperty.query(UserProperty.userId == currUser.user_id()).get()
			if result == None:
				self.response.write('Average Joe!')
				userProp = UserProperty(userId=currUser.user_id(), userName=currUser.nickname(), userStatus="Owner")
				userProp.put()
			else:
				template_values = {
					'name': currUser.nickname(),
					'owners': UserProperty.query(UserProperty.userStatus == "Owner").fetch(10),
					'admins': UserProperty.query(UserProperty.userStatus == "Admin").fetch(10),
					'requests': AccessRequest.query().fetch(10),
				}
				template = JINJA_ENVIRONMENT.get_template('users_template.html')
				self.response.write(template.render(template_values))

class RequestSubmitHandler(webapp2.RequestHandler):
	def get(self):
		currUser = users.get_current_user()
		if currUser == None:
			self.redirect(users.create_login_url(self.request.uri))
		else:
			newRequest = AccessRequest(userName = currUser.nickname(), userId = currUser.user_id(), requestedAccess = "Admin", requestReason = "Cause reasons.")
			newRequest.put()
			self.response.write('Submitted Request')

#
#	AJAX this page with the following params:
#	requestId			- Id of the user making the request	
#	requestName 		- Name of the user making the request
#	requestedStatus		- Status being requested
#	decision 			- Decision that was made, Y or N
#
class RequestDecisionHandler(webapp2.RequestHandler):
	def post(self):
		currUser = users.get_current_user()
		if currUser == None:
			self.response.write('-1')
		else:
			result = UserProperty.query(UserProperty.userId == currUser.user_id()).get()
			if result == None:
				self.response.write('-1')
			else:
				requestId = self.request.POST['requestId']
				requestName = self.request.POST['requestName']
				requestedStatus = self.request.POST['requestedStatus']
				decision = self.request.POST['decision']
				if decision == "Y":
					newUser = UserProperty(userId=requestId, userName=requestName, userStatus=requestedStatus)
					newUser.put()
					currRequest = AccessRequest.query(AccessRequest.userId == requestId).get()
					currRequest.key.delete()
					self.response.write('1')
				else:
					currRequest = AccessRequest.query(AccessRequest.userId == requestId).get()
					currRequest.key.delete()
					self.response.write('0')

app = webapp2.WSGIApplication([
    ('/', MainHandler), ('/users', UsersPageHandler), ('/newrequest', RequestSubmitHandler), ('/requestdecision', RequestDecisionHandler)
], debug=True)