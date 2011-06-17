#!/usr/bin/python

# huge work-in-progress
# given an abstract page, retrieve the names and ids of all of the voters

import re
import urllib2
from BeautifulSoup import BeautifulSoup
url = 'https://mix.oracle.com/events/oow11/proposals/10916-oracle-11gr2-cluster-upgrade-success-story-a-complete-life-cycle'
page = urllib2.urlopen(url)
soup = BeautifulSoup(page)


voters = soup.findAll('a',{"href":re.compile('/events/oow11/voting/view/'),"title":True})

for voter in voters:
	name = voter.get('title').lower()
	id = re.findall(r'\d{3,}',voter.get('href'))[0]
	print name, id