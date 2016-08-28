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
time.sleep(60)
data = json.load(page)
world = data["config"]["time"]
vs = "%s" % data["result"][str(world)]["vs"]
nc = "%s|" % data["result"][str(world)]["nc"]
tr = "%s|" % data["result"][str(world)]["tr"]
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





