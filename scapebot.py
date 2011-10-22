' scapebot is a part of Carl Sagans Laboratories '
' authored by Artur Sapek '

from BeautifulSoup import BeautifulSoup
from mechanize import Browser
import urllib2

months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

class scapebot():

	def command(self):    # Right now this only searches Comet Tavern
		userinput = raw_input('> ')
		self.Comet_Tavern(userinput)
	
	def Comet_Tavern(self, date):
		br = Browser()
		br.open('http://www.comettavern.com/shows.php')
		br.select_form(nr=0)
		month = months[int(date[0:2]) - 1]
		day = ' %s ' % date[2:4]
		br['month'] = [month]
		results = br.submit(name='submit').read()
		soup = BeautifulSoup(results)
		show = []
		found = False
		for main in soup(id='main'):
			for link in main('a'):
				if day in str(link.renderContents()):
					try:
						entry = br.follow_link(text=link.renderContents(), nr=0).read()
						found = True
					except:
						break
		if found == False:	
			show = 'No show on that day'
		else:
			bands = []
			entry = BeautifulSoup(entry)
			for main in entry(id='main'):
				for band in main('li'):
					bandname = band.renderContents()
					for a in band('a'):
						bandname = a.renderContents()
					bands.append(bandname)
			for extrainfo in entry('center'):
				for font in extrainfo('font'):
					for b in font('b'):
						if '$' in b.renderContents():
							extra = b.renderContents()
							time = extra[0 : extra.index(' ')]
							price = extra[extra.index('$') : len(extra)]
			show.append(bands)
			show.append('%s %s' % (month, day[0:3]))
			show.append(time)
			show.append(price)
		print show
		self.command()


	def email(self, To, Subject, Body):    # For emailing critical errors / progress reports
	
		import smtplib
		from email.MIMEMultipart import MIMEMultipart
		from email.MIMEText import MIMEText
		from email.MIMEBase import MIMEBase
		from email.Utils import COMMASPACE, formatdate
		To = [To]
		From = 'scapebot <artur.sapek@gmail.com>'
		assert type(To) == list
		Msg = MIMEMultipart()
		Msg['From'] = From
		Msg['To'] = COMMASPACE.join(To)
		Msg['Subject'] = Subject
		Msg.attach(MIMEText(Body))

		server = smtplib.SMTP('smtp.gmail.com', '587')
		server.ehlo()
		server.starttls()
		server.ehlo()
		server.login('artur.sapek', 'chaney15adick')
		server.sendmail(From, To, Msg.as_string())
		server.quit()

	def twitter(self, action):    # Fun shit
		br = Browser()
		br.set_handle_robots(False) # not spamming or abusing twitter, just using it creatively :)
		br.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.202 Safari/535.1')]		
		br.open('https://mobile.twitter.com/session/new')
		br.select_form(nr=0)
		br.form['username'] = 'scapebot'
		br.form['password'] = 'dubaSNL'
		br.submit()
		
		#logged in

		if action[0] == "tweet":
			br.select_form(nr=0)			
			br['tweet[text]'] = action[1]
			br.submit()

		if action[0] == "search":
			isSearchForm = lambda l: l.action == 'http://mobile.twitter.com/searches'
			br.select_form(predicate=isSearchForm)
			br['search[query]'] = action[1]
			results = br.submit().read()
			soup = BeautifulSoup(results)
			tweets = soup.findAll('div', attrs={'class' : 'list-tweet'} )
			for tweet in tweets:
				sender = tweet.find('strong').a.renderContents()
				message = tweet.find('span', attrs={ 'class' : 'status' } ).renderContents()
				message_soup = BeautifulSoup(message)
				for tag in message_soup.findAll(True):
					if tag.name == 'a':
						hashtag = '%s' % tag.renderContents()
						tag.replaceWith(hashtag)
				message = message_soup
				tweetContents = '@%s %s' % (sender, message)
				print tweetContents
