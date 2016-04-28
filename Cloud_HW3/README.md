Cloud_HW3
=========

Calendar creator using Google AppEngine

Written in Python

### Functionality ###
This web app works as follows:

1. The user is given a Login link upon visiting the page. The user clicks the link and logs into their Google account.

2. Upon entering account information, the user is sent to the main page, which contains a form to fill out for an event that can occur multiple times in one week, an Add Event button, and a Download Calendar File button

3. The user enters event information into the appropriate boxes. The webpage checks to make sure it is formatted correctly.

4. Once the user has finished their event, they press the Add Event button and this event is added to their list of events.

5. The user may repeat steps 3 and 4 multiple times until they are satisfied with their events. Then, once ready, the user presses the Download Calendar File button and is given the option to download the file. Once this button is pressed, all user data is reset.

**tl/dr:** Create multiple recurring events within a week, receive ics file (the week is January 5th, 2015)

### Services ###
This web app uses the following App Engine services:

1. Google User Management: The user logs in and their email is used as a key for memcache.

2. Memcache: Stores the number of events added as well as the string for the event file itself.

### Future Work ###

1. Allow user to input start and end date.

2. Utilize either Mail api or Calendar api to transmit calendar info

3. Generate class schedule using UC's class system

![Photo](https://github.uc.edu/greerji/Cloud_HW3/raw/master/CatalystBender.PNG)
  
