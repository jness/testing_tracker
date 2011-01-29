#!/usr/bin/python
from datetime import datetime, timedelta
from re import compile
from urllib2 import urlopen
import sys

def getrelease():
    req = urlopen('http://dl.iuscommunity.org/pub/ius/testing/Redhat/')
    content = req.read()
    release = compile('alt="\[DIR\]"></td><td><a href="([\d.]*)/">').findall(content)
    return release

def getpackage(release, days):
    req = urlopen('http://dl.iuscommunity.org/pub/ius/testing/Redhat/' + release + '/SRPMS/')
    #req = urlopen('http://dl.iuscommunity.org/pub/ius/testing/Redhat/5/SRPMS/')
    content = req.read()

    packages = compile('<a href=".*src.rpm">(.*).src.rpm</a></td><td align="right">(.*)  </td><td align="right">').findall(content)

    # Define our Month dictionary
    months = {}
    months['Jan'] = 1
    months['Fed'] = 2
    months['Mar'] = 3
    months['Apr'] = 4
    months['May'] = 5
    months['Jun'] = 6
    months['Jul'] = 7
    months['Aug'] = 8
    months['Sep'] = 9
    months['Oct'] = 10
    months['Nov'] = 11
    months['Dec'] = 12

    # the date format for right now
    now = datetime.now().date()
    global rpms
    rpms = {}

    for package in packages:

        timestamp = package[1].split('-')
        day = timestamp[0]
        month = timestamp[1]
        month = months[month]
        year = timestamp[2].split()
        year = year[0]

        date = datetime(int(year), int(month), int(day)).date()
        delta = (now - date)
    
        if delta > timedelta(days = days):
            rpms[package[0]] = delta.days
    return rpms

if len(sys.argv) != 2:
    print """
        Usage:
            """ + sys.argv[0] + """ [days]
          """
    sys.exit(1)

print '-'*55
print '%-10s %s' % ('Age', 'Package')
print '-'*55

# Get our dictionary
for release in getrelease():
    getpackage(release, int(sys.argv[1]))

for package in rpms:
    print '%-10s %s' % (rpms[package], package)
