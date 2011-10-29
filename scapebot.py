' scapebot is a part of Carl Sagans Laboratories '
' authored by Artur Sapek '





from BeautifulSoup import BeautifulSoup, SoupStrainer
from mechanize import Browser
import csv, string


class scapebot():

	def __init__(self):
		global months 
		months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
		global monthsabbr 
		monthsabbr = ['Jan', 'Feb', 'Mar', 'April', 'May', 'June', 'July', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

	def sanitize(self, x): #clean up names which are often not spelled consistently
		for i in range(1, 32):
			x = ''.join(x.split(str(string.punctuation)[i]))
		return x
		

	def command(self):    # Commandline interpreter
		userinput = raw_input('> ')
		self.Comet_Tavern(userinput)

	def scrapeComet(self):
		file = open('shows.csv', 'rb')
		ID = int(len(file.readlines())) - 1
		file.close()
		file = open('shows.csv', 'a')
		
		writer = csv.writer(file)

		for i in range(1, 31):
			addon = ''
			if i < 10:
				addon = '0'
			date = '11' + addon + str(i)
			show = self.Comet_Tavern(date)
			if show:
				ID += 1
				show.insert(0, ID)
				print show
				writer.writerow(tuple(show))

			
		file.close()




	# dealing with a band: checking to see if they exist in the db, if not researching and add them to the db

	# these functions will be used several times per show when scraping shows:


	def checkBand(self, bandname): # checks if a band exists in the db, if not this will redirect to research band
		file = open('bands.csv', 'rb')
		ID = int(len(file.readlines()))
		file.seek(0)
		reader = csv.reader(file)
		bandfound = False
		for row in reader:
			if row[1] == bandname:
				bandfound = True
				return row[0]
				break
		if not bandfound:
			file.close()
			file = open('bands.csv', 'a')
			writer = csv.writer(file)
			writer.writerow((ID, bandname))
			file.close()
			return ID

	def getBand(self, ID):
		file = open('bands.csv', 'rb')
		reader = csv.reader(file)
		rownum = -1
		bandfound = False
		for row in reader:
			rownum += 1
			if rownum == ID:
				return row
				bandfound = True
				break
		if not bandfound:
			return 'No band with that ID'
	
	def researchBand(self, bandname): # will research band if a new entry is required (which will be more often than not for a long time)
		#first things first: Google them.
		br = Browser()
		br.set_handle_robots(False)
		br.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.202 Safari/535.1')]						
		br.open('http://google.com')
		br.select_form(nr=0)
		query = '%s' % bandname
		if len(bandname) / len(bandname.split()) <= 3:
			query = '"%s"' % bandname
		else:
			query = '%s music' % bandname
		br['q'] = query
		soup = BeautifulSoup(br.submit().read())
		results = soup.findAll('ol', attrs={'id': 'rso'})[0]
		sources = {}
		for li in results('li'):
			try:
				for em in li(['em', 'b']):
					em.replaceWith(em.renderContents())
				#print li.div.h3.a.renderContents(), li.div.h3.a['href']

				
				link = li.div.h3.a
				#print link.renderContents()
				#knownSources = {'Wikipedia': 'wikipedia.org', 'Last.fm': 'last.fm/music', 'Facebook': 'facebook.com', 'Bandcamp': 'bandcamp.com', 'Myspace': 'myspace.com', 'Soundcloud': 'soundcloud.com'}
				knownSources = {'Wikipedia': 'wikipedia.org'}
				for entry in knownSources:
					try:
						temp = link['href'].index(knownSources[entry])
						#so it doesn't redefine entries with lower results:
						if entry in sources:
							break
						try:
							#print '.', knownSources[entry], self.sanitize(bandname) 
							#print link['href']
							
							br = Browser()
							br.set_handle_robots(False)
							br.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.202 Safari/535.1')]	
							temp = self.sanitize(str(BeautifulSoup(br.open(link['href']).read())).lower()).index(self.sanitize(bandname).lower())
							try:
								sources[entry] = str(link['href'][:link['href'].index('?')])
							except:
								sources[entry] = str(link['href'])								
						except:
							break
					except:
						pass
			except:
				pass


		print sources
		
		INFO = [bandname,'','','']
		# need to append genre, origin, and album cover

			
		if 'Wikipedia' in sources:
			#scrape wikipedia
			wikiINFO = {}
			wiki_browser = Browser()
			soup = BeautifulSoup(br.open(sources['Wikipedia']).read())
			try:
				originInfo = soup.findAll('th', text='Origin')[0].parent.parent.td
				for link in originInfo('a'):
					link.replaceWith(link.renderContents())
				for citation in originInfo('sup'):
					citation.replaceWith('')
				for linebreak in originInfo('br'):
					linebreak.replaceWith('')
				

				origin = originInfo.renderContents()

				

				wikiINFO['Origin'] = origin

			except:
				origin = False
			# origin done, now do same for Genres
			try:
				
				genreInfo = soup.findAll('th', text='Genres')[0].parent.parent.parent.td
				
				#print genreInfo

				for link in genreInfo('a'):
					link.replaceWith(link.renderContents())
				for citation in genreInfo('sup'):
					citation.replaceWith('')
				for linebreak in genreInfo('br'):
					linebreak.replaceWith('')
				genres = genreInfo.renderContents()

				wikiINFO['Genre'] = genres	
				
			except:
				pass
			# genres done



			



		
		if 'Myspace' in sources:
			pass
			
			


		
		if 'Last.fm' in sources:
			#scrape last.fm
			pass
		if 'Bandscamp' in sources:
			#scrape bandcamp
			pass

		if 'Soundcloud' in sources:
			#scrape soundcloud
			pass



	
		# combine the info collected from all sources
		
		positions = {'Genre':1,'Origin':2,'Albumsrc':3}
		
		

		try:
			for entry in wikiINFO:
				INFO[positions[entry]] = wikiINFO[entry]
		except:
			pass
		return INFO

		
# scraping functions
# format: [ showID, venueID, Date, Time, Price, 21+, Bands ]

	
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
						pass
		if found == False:	
			show = []
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


			show = ['1', '%s %s' % (month, day[0:3]), time, price, 'True']				
			for band in bands:
				show.append(band)
		return show

	def Neumos_Scrape_Upcoming(self):
		br = Browser()
		soup = br.open('http://neumos.com/neumos.php').read()
		soup = BeautifulSoup(soup)
		show = []
		

		events = soup.findAll('p', attrs={ 'class' : 'ShowParagraph' })
		for event in events:
			writtendate = event.span.renderContents()
			writtendate = writtendate[writtendate.index('.')+1:]
			month = writtendate[0:writtendate.index('.')]
			writtendate = writtendate[writtendate.index('.')+1:]
			day = writtendate[0:writtendate.index('.')]
			date = '%s %s' % (months[int(monthsabbr.index(month))], day)
			bands = []
			booze = None
			soldout = event.findAll('span', attrs={ 'class' : 'ShowAlert' })
			otherbands = event.findAll('a', attrs={ 'title' : 'Click for info' } )
			for band in otherbands:
				bands.append(band.renderContents())
			bands = bands[1:] # cut out the first occurrence of the inevitably doubled headliner, less code than other methods
			text = event.find('span', attrs={ 'class' : 'description' })
			desc = text.renderContents()
			
			if not soldout:
				try:
					price = desc[desc.index('$'):]
					price = price[:price.index(' ')]
				except:
					pricefree = desc[desc.index('FREE'):]
					if pricefree:
						price = 'Free'
			else:
				price = 'Sold out'

			time = desc.index('Doors at')
			time = desc[time + 9:]
			time = time[:time.index(' ')]

			try:
				booze = desc.index('21+')
			except:
				pass

			if booze:
				booze = 'True'
			else:
				booze = 'False'
			
			show = ['2', date, time, price, booze]
			for band in bands:
				show.append(band)

			return show

	def Neumos(self, date):
		br = Browser()
		monthgiven = months[int(date[0:2]) - 1]
		soup = BeautifulSoup(br.open('http://neumos.com/neumoscalendar.php?month_offset=').read())
		month = str(soup.findAll('th', attrs={ 'class' : 'CalendarMonth' })[0].renderContents())
		month = month[:month.index(' ')]
		if month != monthgiven:
			while True:
				month = str(soup.findAll('th', attrs={ 'class' : 'CalendarMonth' })[0].renderContents())
				month = month[:month.index(' ')]
				if month != monthgiven:
					soup = BeautifulSoup(br.follow_link(text_regex='next month').read())
				else:
					break
		calendar = soup.findAll('table')[1]
		date_entries = calendar.findAll('td')
		for entry in date_entries:
			if date[2:4] in entry.renderContents()[0:5]:
				break
		try:
			target = ' '.join(str(entry.a.div.renderContents()).split())
			soup = BeautifulSoup(br.follow_link(text=target).read())
			shows = soup.findAll('p', attrs={ 'class' : 'ShowParagraph' })
			temp = []
			showdates = []
			for show in shows:
				writtendate = show.span.renderContents()
				writtendate = writtendate[writtendate.index('.')+1:]
				writtendate = writtendate[writtendate.index('.')+1:]
				day = writtendate[0:writtendate.index('.')][0:2]
				if day != date[2:4]:
					break
				temp.append(show)
			shows = temp
			for event in shows:
				writtendate = event.span.renderContents()
				writtendate = writtendate[writtendate.index('.')+1:]
				month = writtendate[0:writtendate.index('.')]
				writtendate = writtendate[writtendate.index('.')+1:]
				day = writtendate[0:writtendate.index('.')]
				date = '%s %s' % (months[int(monthsabbr.index(month))], day)
				bands = []
				booze = None
				soldout = event.findAll('span', attrs={ 'class' : 'ShowAlert' })
				otherbands = event.findAll('a', attrs={ 'title' : 'Click for info' } )
				for band in otherbands:
					bands.append(band.renderContents())
				bands = bands[1:] # cut out the first occurrence of the inevitably doubled headliner, less code than other methods
				text = event.find('span', attrs={ 'class' : 'description' })
				desc = text.renderContents()
				
				if not soldout:
					try:
						price = desc[desc.index('$'):]
						price = price[:price.index(' ')]
					except:
						pricefree = desc[desc.index('FREE'):]
						if pricefree:
							price = 'Free'
				else:
					price = 'Sold out'

				time = desc.index('Doors at')
				time = desc[time + 9:]
				time = time[:time.index(' ')]

				try:
					booze = desc.index('21+')
				except:
					pass

				if booze:
					booze = 'True'
				else:
					booze = 'False'
				
				show = ['2', date, time, price, booze]
				for band in bands:
					show.append(band)
				print show
		except:
				print 'No show that day.'

			
		
		







	def Stranger_Music_Listings(self):    # For cross-referencing, supplementing information
		br = Browser()
		br.open('http://www.thestranger.com/seattle/Music')
		listings = br.follow_link(text='Music Listings').read()
		listings = BeautifulSoup(listings)
		events = listings.findAll('div', attrs={ 'class' : 'EventListing clearfix' })
		for event in events:
			price = event.find('p')
			try:
				print price.find('strong').renderContents()
			except:
				pass
		pass



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
		password = open('twitterpassword.txt').readline()[0:9]
		br.set_handle_robots(False) # not spamming or abusing twitter, just using it creatively :)
		br.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.202 Safari/535.1')]		
		br.open('https://mobile.twitter.com/session/new')
		br.select_form(nr=0)
		br.form['username'] = 'scapebot'
		br.form['password'] = password
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
				return tweetContents
