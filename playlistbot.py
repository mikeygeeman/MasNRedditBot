#!/usr/bin/env python

import datetime
import OAuth2Util
import praw

print str(datetime.datetime.now()), "Generating Dates"
user = 'PlaylisterBot'
#user = 'mikeygeeman'
start = datetime.datetime.now()
tseven = start - datetime.timedelta(days=7)
fixedstart = start.strftime('%m/%d/%y')
fixeddelta = tseven.strftime('%m/%d/%y')

print str(datetime.datetime.now()), "Generating Message Body"
message = "playlist /r/MasN /r/emeraldps2 "+fixeddelta+' '+fixedstart+' new created EmeraldPs2 Week in Review'
newmessage = "playlist /r/MasN /r/Planetside "+fixeddelta+" "+fixedstart+" new created Planetside Week in Review"


print str(datetime.datetime.now()), "Sending Messages to ", user
r = praw.Reddit("GfunkyStuff_1.1.0")
o = OAuth2Util.OAuth2Util(r, print_log=True)
o.refresh(force=True)
r.send_message(user, 'PlaylistRequest', message)
r.send_message(user, 'PlaylistRequest', newmessage)

print str(datetime.datetime.now()), "Messages sent to ", user





