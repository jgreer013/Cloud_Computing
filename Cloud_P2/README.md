Cloud_P2
=========

This software allows users to build a schedule file for their classes that they can add to either their iCalendar or Google Calendar via importing an ICS file.

Written in Python

WARNING: This app may take awhile if too many classes are added, as it generates EVERY combination of the sections for those classes.

### Functionality ###
This web app works as follows:

1. The user is given a Login link upon visiting the page. The user clicks the link and logs into their Google account.

2. Upon entering account information, the user is sent to the main page, which contains a form to enter in class names such as CS2011, with each class being entered on a new line.

3. The user enters event information into the appropriate box. The webpage checks to make sure it is formatted correctly.

4. Once the user has added their classes, a list of all combinations of classes is generated and displayed, with only the valid combinations being displayed.

5. The user can read through the combinations and select one which they prefer. They then click the Email ICS File button, and the file is emailed to them as an attachment.

**tl/dr:** Add class ID's, return and have schedule emailed to you

### Services ###
This web app uses the following App Engine services:

1. Google User Management: The user logs in and their email is used to receive emails.

2. Google Mail: Emails the file to the user

3. Task Queue: Too many classes exceeded 60s limit, switched to Task Queue to offload processing

4. Memcache: Access memcache for storing html text for later display

Source of gif file:
https://www.google.com/url?sa=i&rct=j&q=&esrc=s&source=images&cd=&ved=0ahUKEwiW-vXEyb7LAhXGKh4KHcyCC10QjBwIBA&url=https%3A%2F%2Ffarm7.staticflickr.com%2F6107%2F6327271833_c27df8ec48_o_d.gif&psig=AFQjCNG_scCmNF0esvY-oDvJHsYgltrPvA&ust=1457989818463111&cad=rjt

![Photo](https://github.uc.edu/bakerfn/cs6065-p2/raw/master/CatalystBender.PNG)
  
