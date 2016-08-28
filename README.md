This is a reddit bot designed to scrape pages with BeautifulSoup and then update a reddit sidebar useing praw and oAuth2


You will need to use several different pip installs to make this work
BeauttifulSoup
praw
praw-OAuth2Utils

Once you download these you will need to go to reddit /pref/apps and create your app.

Run Demo.py to set your permissions for the first token refresh.

From there you can run sidebar.py and it will go out refresh the token and run the scrip against the differnet urls.

It then puts the list together and submits it to the reddit wiki config/sidebar.

USe at your own risk.
