#!/usr/bin/env python

import cgi

form = cgi.FieldStorage()
searchterm =  form.getvalue('eName')
print searchterm
