#!/usr/bin/env python


import webapp2
from fileBuild import addEvent

from google.appengine.api import users
from google.appengine.api import memcache

import time


class MainPage(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()
    fn = open('index.html','r')
    html_page = fn.read()
    fn.close()
    if user:
      self.response.out.write("Welcome, " + user.nickname() + "<br></br>")
      count = memcache.get(str(user.email()))
      if count == None:
        self.response.out.write("You have added 0 events.<br></br>")
        memcache.set(str(user.email()), 0)
        memcache.set(str(user.email()) + 'events', "BEGIN:VCALENDAR\n" + "VERSION:2.0\n" + "PRODID:-//hacksw/handcal//NONSGML v1.0//EN\n" + "CALSCALE:GREGORIAN\n")
      else:
        self.response.out.write("You have added " + str(count) + " events.<br></br>")
      self.response.out.write(html_page)
    else:
      self.response.out.write('<a href="' + users.create_login_url('/'))
      self.response.out.write('">Login</a>')

class SubPage(webapp2.RequestHandler):
  def post(self):
    user = users.get_current_user()
    event_name = self.request.get('eName')
    event_start = self.request.get('start')
    event_end = self.request.get('end')
    event_days = self.request.get_all('Days[]')
    count = memcache.get(str(user.email()))
    memcache.set(str(user.email()), int(count) + 1)
    prev = memcache.get(str(user.email()) + 'events')
    memcache.set(str(user.email()) + 'events', addEvent(event_name, event_start, event_end, event_days, prev))
    self.redirect('/')

class icsPage(webapp2.RequestHandler):
  def post(self):
    user = users.get_current_user()
    self.response.headers['Content-Type'] = 'text/calendar; charset=utf-8'
    self.response.headers['Content-Disposition'] = 'attachment; filename=event.ics'
    self.response.out.write(memcache.get(user.email() + 'events') + 'END:VCALENDAR\n')
    memcache.set(str(user.email()), 0)
    memcache.set(str(user.email()) + 'events', "BEGIN:VCALENDAR\n" + "VERSION:2.0\n" + "PRODID:-//hacksw/handcal//NONSGML v1.0//EN\n" + "CALSCALE:GREGORIAN\n")

app = webapp2.WSGIApplication([
  ('/', MainPage),
  ('/test.py', SubPage), # test.py doesn't exist, this just runs the code necessary to add an event to memcache
  ('/send.py', icsPage), # send.py doesn't exist, this just runs the code necessary to give the file to the user.
], debug=True)
