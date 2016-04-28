#!/usr/bin/env python
# Frazier Baker & Jeremiah Greer
# For CS6065 Project. March 2016
####################################

import webapp2
from google.appengine.api import users,mail,memcache
import calendar
#import ucclasses as uc
import re
from unicodedata import normalize
import csvAccess
import classDict
import validatePermute 
import schedInfo
import fileBuild
from google.appengine.api import users,mail,taskqueue,memcache

class MainPage(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()
    if user:
      index = open("index.html","r")
      self.response.write(index.read())
    else:
      self.response.out.write('<a href="' + users.create_login_url('/'))
      self.response.out.write('">Login</a>')
    #uc.getPermutations
    #offer permutations via html
  def post(self):
    #Create a task
    user = users.get_current_user()
    if user:
      if "classes" in self.request.POST:
        (classD,sectD) = classDict.buildClassDict()
          #Capital D in honor of Mr. Daniels
        classList = self.request.get("classes",default_value=None) #List of classes from user, separated by commas
        classes = re.split("\W",classList) #Lots of delimiters
        classes = [x.encode("ascii") for x in classes]
        classes = [x for x in classes if x] #removing emptystring
        #http://stackoverflow.com/questions/18272066/easy-way-to-convert-a-unicode-list-to-a-list-containing-python-strings
        memcache.set(user.user_id(),"/working.gif")
        hi = taskqueue.add(url="/worker",params={"key":user.user_id(),"classes":",".join(classes)})
        print "LAUNCHING WORKER"+str(hi)
        self.redirect("/showInfo?id="+user.user_id())
    else:
      self.response.write("<html><body>")
      self.response.out.write('<a href="' + users.create_login_url('/'))
      self.response.out.write('">Login</a>')
    self.response.write("</body></html>")

class ShowInfoPage(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()
    if ("id" in self.request.GET) and user:
      if user.user_id() == self.request.get("id"):
        if memcache.get(user.user_id()) == "/working.gif":
          self.response.write("<html><head></head><body>"+
          "<img src='/working.gif' />"+
          "<script type='text/javascript'>"+
          "setTimeout(function(){location.reload()},10000);"+
          "</script>"+
          "</body></html>")
        else:
          self.response.write(memcache.get(user.user_id()))
      else:
        self.response.write("Login Error")
    else:
      self.response.write("HTTP 403 Forbidden")
      return 403

class WorkerPage(webapp2.RequestHandler):
  def post(self):
    classes = ""
    key = "default"
    if "classes" in self.request.POST and "key" in self.request.POST:
      key = self.request.get("key")
      (classD,sectD) = classDict.buildClassDict()
        #Capital D in honor of Mr. Daniels
      classList = self.request.get("classes",default_value=None) #List of classes from user, separated by commas
      classes = re.split("\W",classList) #Lots of delimiters
      classes = [x.encode("ascii") for x in classes]
      classes = [x for x in classes if x] #removing emptystring
      #http://stackoverflow.com/questions/18272066/easy-way-to-convert-a-unicode-list-to-a-list-containing-python-strings
    else:
      return 404
    try:
       meccastring=("<html><head><style type='text/css'>"+
          "td,th { border:1px solid black; }"+
          "</style></head><body>"+"<iframe style='opacity:0;width:0px;"+
           "height:0px;' name='invisible' id='invisible'></iframe>")
       combos = csvAccess.comb(classes,classD)
       for platter in combos:
         if not validatePermute.valTogether(platter):
           continue
         meccastring+=("<table style='border:3px solid"+
           "#000;text-align:center;'>")
         meccastring+=("<tr>")
         meccastring+=("<th>Class</th>")
         meccastring+=("<th>Meeting Days</th>")
         meccastring+=("<th>Meeting Times</th>")
         meccastring+=("<th>Dates</th>")
         for i in xrange(len(classes)):
           entree = platter[i]
           info = schedInfo.getSchedInfo(entree,(classD,sectD))
           meccastring+=("<tr>")
           meccastring+=("<td rowspan='"
             +str(len(info))+"'>"+str(classes[i])+"<br />("+
             str(entree)+
             ")</td>")
           for infobloc in info:
             if infobloc is not info[0]:
               meccastring+=("<tr>")
             meccastring+=("<td>"+"-".join(infobloc[2])+"</td>")
             meccastring+=("<td>"+"-".join(infobloc[1])+"</td>")
             meccastring+=("<td>"+"-".join(infobloc[0])+"</td>")
             meccastring+=("</tr>")
         meccastring+=("</table>")
         meccastring+=(
           "<form action='download' method='post' target='invisible'>"+
           "<input type='hidden' name='choice'"+
           "value='"+",".join(platter)+"' /><input type='submit'"+
           "value='Email ICS File' /><br/><br/>")
    except KeyError as e:
      meccastring+=(str(e)+" is an invalid class name for this semester.")
    memcache.set(key,meccastring)

class DownloadPage(webapp2.RequestHandler):
  def post(self):
    user = users.get_current_user()
    classD, sectD = classDict.buildClassDict()
    sects = self.request.get("choice").encode("ascii","ignore").split(",")
    fc = fileBuild.buildFile(sects, sectD)
    mail.send_mail("Do_Not_Reply@uc-sched.appspotmail.com", str(user.email()), "Class Schedule Download", "Import this file into your preferred calendar. DO NOT add the event through this email, as it does not recognize all events in the file. For instructions on how to import ics files, here are a few links:\n\nGoogle Calendar: https://support.google.com/calendar/answer/37118?hl=en\nApple Calendar: https://support.apple.com/kb/PH11524?locale=en_US\nOutlook: http://windows.microsoft.com/en-us/windows/outlook/calendar-import-vs-subscribe", attachments=[("classSchedule.ics"), (fc)])

app = webapp2.WSGIApplication([('/showInfo',ShowInfoPage),('/worker',WorkerPage),
  ('/', MainPage),("/download", DownloadPage)], debug=True)

