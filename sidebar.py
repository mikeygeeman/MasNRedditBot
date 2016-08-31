#!/usr/bin/env python
# import our goodies
import urllib2
from bs4 import BeautifulSoup
import praw
from datetime import datetime
import json
import time
import OAuth2Util
i = datetime.now()
print str(datetime.now()), "MasNRedditbot Waking Up"

#Get the Data from Fisu
print str(datetime.now()), "Getting Outfit Information"
url = 'http://ps2.fisu.pw/outfit/?name=Masn'
page=urllib2.urlopen(url)
soup = BeautifulSoup(page.read(), 'html.parser')
table = soup.find_all('b')


#Write the dynamic part of the header
print str(datetime.now()), "Generating Template"
textToReplace = "## **About Us**\n"
textToReplace += "**This is the Planetside 2 official site of the MasN outfit.  We are a casual group of players that like to have fun and have people online at all hours**.\n"
textToReplace += "\n"
textToReplace += "## **TeamSpeak 3 Server**\n"
textToReplace += "* **Server: masnts.tsdns.info**\n"
textToReplace += "* **Password: bricklayer**\n"
textToReplace += "**[Connect Now](ts3server://masnts.tsdns.info?nickname=ChangeYourName&password=bricklayer&addbookmark=1 \"MasN Autolink\")**\n"
textToReplace += "\n"
textToReplace += "## **Our Stats**\n"
textToReplace += "Information|Details\n"
textToReplace += ":-:|:-:\n"
textToReplace += "Tag|%s\n" % table[0].get_text()
textToReplace += "Server|%s\n" % table[1].get_text()
textToReplace += "Faction|%s\n" % table[2].get_text()
#textToReplace += "Leader|%s\n" % table[3].get_text()
textToReplace += "Member Count|%s\n" % table[4].get_text()
textToReplace += "Currently Online|%s\n" % table[5].get_text()
textToReplace += "Total Score|%s\n" % table[6].get_text()
textToReplace += "Average BR|%s\n" % table[8].get_text()
textToReplace += "Average SPM|%s\n" % table[9].get_text()
textToReplace += "Average K/D|%s\n" % table[10].get_text()
textToReplace += "Total Time Played|%s\n" % table[11].get_text()
textToReplace += "Average Time Played|%s\n" % table[12].get_text()
textToReplace += "\n"

#get server pops
print str(datetime.now()), "Collecting Emerald Population"
url = 'http://ps2.fisu.pw/api/population/?world=17'
page=urllib2.urlopen(url)
time.sleep(10)
data = json.load(page)
vs = "%s" % data["result"][0]["vs"]
nc = "%s|" % data["result"][0]["nc"]
tr = "%s|" % data["result"][0]["tr"]
textToReplace += "## **Emerald Population**\n"
textToReplace += "TR|NC|VS\n"
textToReplace += ":-:|:-:|:-:\n"
textToReplace += "%s" % tr+nc+vs
textToReplace += "\n"

#fetch the online members
print str(datetime.now()), "Collecting Online Member Information"
url = 'http://ps2.fisu.pw/outfit/?name=Masn'
page=urllib2.urlopen(url)
soup = BeautifulSoup(page.read(), 'html.parser')
data = soup.find_all('tr', {'class': 'online'})
textToReplace += "## **Online Now**\n"
textToReplace += "Name|BR\n"
textToReplace += ":-:|:-:\n"
for row in data:
        name = "%s|" % row.find('td', {'id': 'name'}).get_text()
        battlerank = "BR %s\n" % row.find('td', {'id': 'battlerank'}).get_text()
        textToReplace += name+battlerank
#    textToReplace += "* %s\n" % row.find('td', {'id': 'name'}).get_text()
textToReplace += "\n"
fileToSearch = "/Users/MattsHome/code/template.txt"

#grab the template for the rest
print str(datetime.now()), "Grabbing the Template"
with open('/Users/MattsHome/code/template.txt', 'r') as file :
        filedata=file.read()

#connect to reddit and post
print str(datetime.now()), "Connecting to Reddit"
r = praw.Reddit("your agent")
o = OAuth2Util.OAuth2Util(r, print_log=True)

o.refresh(force=True)
sub = "MasN"
settings = r.get_settings(sub)
# grabs current sidebar
#sidebar_contents = settings['description']
sidebar_contents = textToReplace
sidebar_contents += filedata
r.update_settings(r.get_subreddit(sub), description=sidebar_contents)
print str(datetime.now()), "Updated Reddit!!"

print str(datetime.now()), "Getting Information from Instant Action Podcast"
url = 'http://www.instantactionpodcast.com/category/podcast/feed/'
page=urllib2.urlopen(url)
soup = BeautifulSoup(page.read(), 'html.parser')
raw = soup.find('item')
title = raw.find('title').get_text()
link = raw.find('link').get_text()
description = raw.find('description').get_text()

print str(datetime.now()), "Connecting to Reddit to fetch lat 100 posts"
subreddit = r.get_subreddit('MasN')
for submission in subreddit.get_hot(limit =100):
    if title in submission.title:
        print str(datetime.now()), "The most recent copy has already been posted, exiting"
        exit()
    else:
        continue
print str(datetime.now()), "New Feed Detected"

print str(datetime.now()), "Posting link to Reddit"
subreddit.submit(title, url=link)
print "Posted to Reddit"




