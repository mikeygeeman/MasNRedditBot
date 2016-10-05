#!/usr/bin/env python
# import our goodies
import urllib2
from bs4 import BeautifulSoup
import praw
from datetime import datetime
import json
import OAuth2Util
import time
import traceback
import sqlite3
from praw.handlers import MultiprocessHandler
i = datetime.now()
print str(datetime.now()), "MasNRedditbot Waking Up"

#Get the Data from Fisu
print str(datetime.now()), "Getting Outfit Information"
url = 'http://ps2.fisu.pw/outfit/?name=Masn'
page=urllib2.urlopen(url)
soup = BeautifulSoup(page.read(), 'html.parser')
table = soup.find_all('b')


#Write the dynamic part of the header
try:
    print str(datetime.now()), "Generating Template"
    textToReplace = "## **TeamSpeak 3 Server**\n"
    textToReplace += "Server|Password\n"
    textToReplace += ":-:|:-:\n"
    textToReplace += "masnts.tsdns.info|bricklayer\n"
    textToReplace += "**[Connect Now](ts3server://masnts.tsdns.info?nickname=ChangeYourName&password=bricklayer&addbookmark=1 \"MasN Autolink\")**\n"
    textToReplace += "\n"
    whoa = "Tag|%s\n" % table[0].get_text()
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
except:
    pass
#get server pops

print str(datetime.now()), "Collecting Emerald Population"
url = 'http://ps2.fisu.pw/api/population/?world=17'
page = urllib2.urlopen(url)
time.sleep(10)
data = json.load(page)
#world = data["config"]["time"]
vs = "[%s](/vspop)" % data["result"][0]["vs"]
nc = "[%s](/ncpop)|" % data["result"][0]["nc"]
tr = "[%s](/trpop)|" % data["result"][0]["tr"]
textToReplace += "## **Emerald Population**\n"
textToReplace += "[ ](/trlogo)|[ ](/nclogo)|[ ](/vslogo)\n"
textToReplace += ":-:|:-:|:-:\n"
textToReplace += "%s" % tr+nc+vs
textToReplace += "\n"
#fetch the online members

try:
    print str(datetime.now()), "Collecting Online Member Information"
    url = 'http://ps2.fisu.pw/outfit/?name=Masn'
    page=urllib2.urlopen(url)
    soup = BeautifulSoup(page.read(), 'html.parser')
    data = soup.find_all('tr', {'class': 'online'})
    whoa = "Tag|%s\n" % table[0].get_text()
    textToReplace += "## **Online Now**\n"
    textToReplace += "Name|BR\n"
    textToReplace += ":-:|:-:\n"
    for row in data:
            name = "[%s]" % row.find('td', {'id': 'name'}).get_text()
            link = "(http://ps2.fisu.pw/player/?name=%s&show=statistics)|" % row.find('td', {'id': 'name'}).get_text()
            battlerank = "BR %s\n" % row.find('td', {'id': 'battlerank'}).get_text()
            textToReplace += name+link+battlerank
    #    textToReplace += "* %s\n" % row.find('td', {'id': 'name'}).get_text()
    textToReplace += "\n"
    fileToSearch = "/Users/MattsHome/code/template.txt"
except:
    pass

#grab the template for the rest
print str(datetime.now()), "Grabbing the Template"
with open('/Users/MattsHome/code/template.txt', 'r') as file :
        filedata=file.read()

#connect to reddit and post
print str(datetime.now()), "Connecting to Reddit"
try:
    handler = MultiprocessHandler('192.168.0.11', 65000)
    r = praw.Reddit("GfunkyStuff_1.1.0", handler=handler)
    o = OAuth2Util.OAuth2Util(r, print_log=True)
except:
    exit()

sub = "MasN"
settings = r.get_settings(sub)
# grabs current sidebar
#sidebar_contents = settings['description']
sidebar_contents = textToReplace
sidebar_contents += filedata
r.update_settings(r.get_subreddit(sub), description=sidebar_contents)
print str(datetime.now()), "Updated Reddit Sidebar!!"

''' USER CONFIG '''

SUBREDDIT = "MasN"
# This is the sub or list of subs to scan for new posts. For a single sub, use "sub1".
# For multiple subs, use "sub1+sub2+sub3+...". For all use "all"

WIKI_PAGE_PREFIX = ''
# This text will prefix the user's name in their wiki page URL.
# If the prefix has a slash at the end, it will become a "folder" of pages.
# Take a look at the "bios" folder here: https://www.reddit.com/r/goldtesting/wiki/pages
# This is done with a prefix of 'bios/'

MESSAGE_INITIAL_SUBJECT = 'Welcome to /r/_subreddit_, _author_!'
MESSAGE_INITIAL_BODY = '''
Hey _author_,

This is the first time we've seen you post in /r/_subreddit_, welcome!

Your [first submission](_permalink_) has been added to your new bio page
at /r/_subreddit_/wiki/_author_.
'''

MESSAGE_UPDATE_SUBJECT = 'Your /r/_subreddit_ bio has been updated'
MESSAGE_UPDATE_BODY = '''
Hey _author_,

Your [submission](_permalink_) to /r/_subreddit_ has been added
to the bottom of your bio at /r/_subreddit_/wiki/_author_.
'''

MESSAGE_FULL_SUBJECT = 'Your /r/_subreddit_ bio is full!'
MESSAGE_FULL_BODY = '''
Hey _author_,

I attempted to update your bio page at /r/_subreddit_/wiki/_author_,
but found that it was too full for me to add more text!
'''
# The subject and body of the messages you will to send to users.
# If you put _author_ in either one of these texts, it will be automatically
# replaced with their username.
# Feel free to send me a message if you want more injectors

WIKI_PAGE_INITIAL_TEXT = '''

This is the bio page for /u/_author_

'''
# When creating a user's wiki page, put this text at the top.

WIKI_POST_FORMAT = '''

---

**[_title_](_permalink_)**

_text_
'''
# The format used when putting the submission text into user's wiki page
# If it's a linkpost, then _text_ will be the link they submitted.
# This one puts a horizontal line above each post to separate them
# Available injectors are _title_, _permalink_, _text_

WIKI_PERMLEVEL = 1
# Who can edit this page?
# 0 - Use global wiki settings
# 1 - Use a whitelist of names
# 2 - Only mods can read and see this page

MAXPOSTS = 10
# How many submissions / how many comments to get on each run
# PRAW can get up to 100 in a single call

MAX_MAILTRIES = 15
# The maximum number of times to attempt sending mail
# in the event of server outage etc.

WAIT = 30
# How many seconds to wait between runs.
# The bot is completely inactive during this time.

''' All done! '''

sql = sqlite3.connect('biowiki.db')
cur = sql.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS users(name TEXT, submissions TEXT)')
cur.execute('CREATE INDEX IF NOT EXISTS userindex on users(name)')
sql.commit()

print('Logging in')
handler = MultiprocessHandler('192.168.0.11', 65000)
r = praw.Reddit("GfunkyStuff_1.1.0", handler=handler)
o = OAuth2Util.OAuth2Util(r, print_log=True)


START_TIME = time.time()


def get_page_content(pagename):
    subreddit = r.get_subreddit(SUBREDDIT)
    try:
        page = subreddit.get_wiki_page(pagename)
        page = page.content_md
    except praw.errors.NotFound:
        page = ''

    return page


def send_message(recipient, subject, body):
    for x in range(MAX_MAILTRIES):
        try:
            print('\tSending mail')
            return r.send_message(recipient, subject, body)
            return
        except praw.errors.HTTPException as e:
            if isinstance(e, praw.errors.NotFound):
                return
            if isinstance(e, praw.errors.Forbidden):
                return
            time.sleep(20)


def update_wikipage(author, submission, newuser=False):
    '''
    Given a username and Submission object, publish a wiki page
    under their name containing the selftext of the post.
    If the wikipage already exists just put the text underneath
    the current content.
    '''

    print('\tChecking current page')
    pagename = WIKI_PAGE_PREFIX + author
    content = get_page_content(pagename)
    if content == '':
        content = WIKI_PAGE_INITIAL_TEXT.replace('_author_', author)
    newtext = WIKI_POST_FORMAT
    newtext = newtext.replace('_title_', submission.title)
    newtext = newtext.replace('_permalink_', submission.short_link)
    if submission.is_self:
        newtext = newtext.replace('_text_', submission.selftext)
    else:
        newtext = newtext.replace('_text_', submission.url)

    if newtext not in content:
        complete = content + newtext
    else:
        complete = content

    print('\tUpdating page text')
    subreddit = r.get_subreddit(SUBREDDIT)
    try:
        subreddit.edit_wiki_page(pagename, complete)
    except praw.errors.PRAWException as e:
        if e._raw.status_code in [500, 413]:
            print('\tThe bio page for %s is too full!')
            return 'full'
        else:
            raise e
    if newuser is True:
        print('\tAssigning permission')
        page = subreddit.get_wiki_page(pagename)
        page.edit_settings(permlevel=WIKI_PERMLEVEL, listed=True)
        page.add_editor(author)
    return True


def biowikibot():
    '''
    - watch /new queue
    - If a new user is found:
        - Create his wiki page
        - Add the Submission's text as the page text
        - Set permissions for him to edit
        - PM him with a link to the page
    - If an existing user is found:
        - Add permalink to the Submission at the bottom of his wiki page.
        - PM him to notify of the update.
    '''

    print('Checking /r/%s/new' % SUBREDDIT)
    subreddit = r.get_subreddit(SUBREDDIT)
    new = list(subreddit.get_new(limit=MAXPOSTS))
    new.sort(key=lambda x: x.created_utc)

    for submission in new:
        if submission.author is None:
            # Post is deleted. Ignore
            continue
        if submission.created_utc < START_TIME:
            # Post made before the bot started. Ignore
            continue
        author = submission.author.name
        cur.execute('SELECT * FROM users WHERE name=?', [author])
        fetch = cur.fetchone()

        if fetch is None:
            print('New user: %s' % author)
            posts = submission.fullname
            cur.execute('INSERT INTO users VALUES(?, ?)', [author, posts])
            result = update_wikipage(author, submission, newuser=True)

            subject = MESSAGE_INITIAL_SUBJECT
            body = MESSAGE_INITIAL_BODY
        else:
            posts = fetch[1].split(',')
            if submission.fullname in posts:
                # Already processed this post. Ignore
                continue
            print('Returning user: %s' % author)
            posts.append(submission.fullname)
            posts = ','.join(posts)
            cur.execute('UPDATE users SET submissions=? WHERE name=?',
                        [posts, author])
            result = update_wikipage(author, submission, newuser=False)

            subject = MESSAGE_UPDATE_SUBJECT
            body = MESSAGE_UPDATE_BODY

        if result == 'full':
            subject = MESSAGE_FULL_SUBJECT
            body = MESSAGE_FULL_BODY

        subject = subject.replace('_author_', author)
        subject = subject.replace('_subreddit_', SUBREDDIT)
        body = body.replace('_author_', author)
        body = body.replace('_permalink_', submission.short_link)
        body = body.replace('_subreddit_', SUBREDDIT)
        if result is not None:
            send_message(author, subject, body)

        sql.commit()
biowikibot()

print('Completed BiowikiRun')

print str(datetime.now()), "Getting Information from Instant Action Podcast"
url = 'http://www.instantactionpodcast.com/category/podcast/feed/'
page=urllib2.urlopen(url)
soup = BeautifulSoup(page.read(), 'html.parser')
raw = soup.find('item')
title = raw.find('title').get_text()
link = raw.find('link').get_text()
description = raw.find('description').get_text()

print str(datetime.now()), "Connecting to Reddit to fetch last 100 posts"
subreddit = r.get_subreddit('MasN')
for submission in subreddit.get_hot(limit =100):
    if title in submission.title:
        print str(datetime.now()), "The most recent copy has already been posted, exiting"
        exit()
    else:
        continue
print str(datetime.now()), "New Feed Detected"

print str(datetime.now()), "Posting link to Reddit"
try:
    subreddit.submit(title, url=link)
except:
    pass
print "Posted to Reddit"