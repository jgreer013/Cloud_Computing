#!/usr/bin/env python


#import datetime
import webapp2

#from google.appengine.api import users


class MainPage(webapp2.RequestHandler):
  def get(self):
    self.response.out.write('<html><body><h1>Hey</h1></body></html>')




app = webapp2.WSGIApplication([
  ('/', MainPage),
], debug=True)
