' scapebot is a part of Carl Sagans Laboratories '
' authored by Artur Sapek '





from BeautifulSoup import BeautifulSoup, SoupStrainer
from mechanize import Browser
from collections import defaultdict
import csv
import string
import re




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
			#	print show
				writer.writerow(tuple(show))

			
		file.close()




	# dealing with a band: checking to see if they exist in the db, if not researching and add them to the db

	# these functions will be used several times per show when scraping shows:


	# hangs up on Facebook pages

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
		# set some quality-assurance variables :) <3
		nameFormatted = False
		GENRES = []

		
		# OKAY. first things first: Google them.
		br = Browser()
		br.set_handle_robots(False)
		br.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.202 Safari/535.1')]						
		br.open('http://google.com')

		br.select_form(nr=0)
		query = '%s' % bandname
		if len(bandname) / len(bandname.split()) <= 3:
			query = '"%s"' % bandname
			wuLyfCoefficient = False
		else:
			query = '%s' % bandname
			wuLyfCoefficient = True
		br['q'] = query
		soup = BeautifulSoup(br.submit().read())
		results = soup.findAll('ol', attrs={'id': 'rso'})[0]
		sources = {}
		try:
			suggestion = soup.findAll('p', attrs={ 'class' : 'sp_cnt' })[0].a
			for i in suggestion('i'):
				i.replaceWith(i.renderContents())
			for b in suggestion('b'):
				b.replaceWith(b.renderContents())
			suggestion = suggestion.renderContents().replace('"', '').replace('- ', '-').replace('&quot', '').replace(';', '')
			bandname = suggestion
		#	print bandname, ' < suggested'
		except:
			pass
		

		


		for li in results('li'):
			try:
				for em in li(['em', 'b']):
					em.replaceWith(em.renderContents())
				#print li.div.h3.a.renderContents(), li.div.h3.a['href']

				#print li.a.renderContents() 
				link = li.div.h3.a
				#print link.renderContents()
				knownSources = {'Wikipedia': 'wikipedia.org', 'Last.fm': 'last.fm/music', 'Facebook': 'facebook.com', 'Bandcamp': 'bandcamp.com', 'Myspace': 'myspace.com', 'Soundcloud': 'soundcloud.com'}
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
							if re.search(bandname.replace(' ', '[ -]'), str(BeautifulSoup(br.open(link['href']).read())), flags=re.I):
								try:
									URL = str(link['href'][:link['href'].index('?')])
									sources[entry] = URL
								except:
									URL = str(link['href'])
									sources[entry] = URL
							if entry == 'Last.fm': # make sure to go to the artist's root page and not videos or something
								m = re.match('http://www.last.fm/music/[^/]*', sources[entry])
								if m:
									sources[entry] = m.group(0)
						except:
							break
					except:
						pass
			except:
				pass


	#	print sources
	
		# need to append genre, origin, and album cover

			
		if 'Wikipedia' in sources:
			#scrape wikipedia
			wikiINFO = {}
			soup = BeautifulSoup(br.open(sources['Wikipedia']).read())
		#	print 'wiki'

			try:
				#redefine bandname with formatting from wiki header, band names can be weird, number 1 trusted source for name formatting

				bandname = soup.h1.renderContents().replace(' (musician)', '').replace(' (band)', '')			
				nameFormatted = True # name formatting done, that was easy :)
			#	print 'title changed from wikipedia'
				originInfo = soup.findAll('th', text='Origin')[0].parent.parent.td
				for link in originInfo('a'):
					link.replaceWith(link.renderContents())
				for span in originInfo('span'):
					span.replaceWith(span.renderContents())
				for citation in originInfo('sup'):
					citation.replaceWith('')
				for linebreak in originInfo('br'):
					linebreak.replaceWith('')
				

				origin = originInfo.renderContents()

				

				wikiINFO['Origin'] = origin

			except:
				pass
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
				genres = genreInfo.renderContents().split(', ')
				

				
				# dealing with newlines:

				if genres[0].find('\n') > -1 and len(genres) == 1:
					genres = re.sub('\n', ', ', genres[0]).split(', ')

					
				genres = self.cleanGenres(genres, bandname)

				wikiINFO['Genre'] = genres	
				
				GENRES += genres

				print 'WIKI genres', genres
				
			except:
				pass
			# genres done



		if 'Last.fm' in sources:
			

			try:
				#scrape last.fm
				lastfmINFO = {}
				soup = BeautifulSoup(br.open(sources['Last.fm']).read())
			#	print 'last.fm'
				
				try:
					soup = str(soup)
					genreMeta = soup.index('itemprop="keywords"') # this is a hack, cos for some reason BeauSoup doesnt find itemprop attrs
					genres = soup[genreMeta + 29:]
					genres = genres[:genres.index('">')]
					genres = genres.split(', ')
					if not nameFormatted:
						nameMeta = soup.index('itemprop="name"')
						bandname = soup[nameMeta + 16:]
						bandname = bandname[:bandname.index('</h1>')]
					#	print 'name reformatted from last.fm'
						nameFormatted = True
						
					# sometimes last.fm will have a band/musician's own name as a tag
					genres = self.cleanGenres(genres, bandname)
					
				except:
					pass

				# origin

				
				try:
				#	print 'origin from lastfm'
					soup = str(soup)
					localityInd = soup.index('p class="origin"') # also a hack, fuckall
					locality = soup[localityInd:]
					locality = locality[locality.find('<strong>') + 8:]
					locality = locality[:locality.index('\n')]
				#	print 'last.fm origin: ', locality
						
				except:
					pass

			#	print 'LAST.FM genres', genres

				lastfmINFO['Genre'] = genres
				if locality != '</strong>':
					lastfmINFO['Origin'] = locality

				GENRES += genres

			except:
				pass
		
		
		if 'Myspace' in sources:
		#	print 'myspace'
			myspaceINFO = {}
			soup = BeautifulSoup(br.open(sources['Myspace']).read())
			
			# myspace is not valid for formatting the bandname, for no good reason they are often in all-caps
			try:	
				target = soup.findAll(attrs={'class':'odd BandGenres'})[0]
				for tag in target.findAll(True):
					tag.replaceWith(tag.renderContents())
				target = target.renderContents()[8:]
				genres = self.cleanGenres(target.split(' / '), bandname)
			#	print 'MYSPACE genres', genres
				GENRES += genres
			except:
				pass
		
		if 'Soundcloud' in sources:
			#scrape soundcloud
		#	print 'soundcloud'

			soundcloudINFO = {}
			soup = BeautifulSoup(br.open(sources['Soundcloud']).read())

		if 'Bandscamp' in sources:
			#scrape bandcamp
			pass

			

		INFO = [bandname,'','','']

		temp = []

		for genre in GENRES:
			# remove vague BS
			if genre not in ['Rock', 'Alternative', 'Indie', 'Electronic music', 'Jazz']:
				temp.append(genre)

		# migrate descriptive genres, abandon the rest

		GENRES = temp

		for genre in GENRES:
			if GENRES.count(genre) > 1:
				GENRES.remove(genre)


		try:
			INFO[1] = self.cleanGenresFinal(GENRES, wikiINFO)
		except:
			INFO[1] = self.cleanGenresFinal(GENRES, {})

		try:
			INFO[2] = self.cleanOrigin(wikiINFO['Origin'])
		except:
			pass

		if INFO[2] == '':
			try:
				INFO[2] = self.cleanOrigin(lastfmINFO['Origin'])
			except:
				pass
		
	
		# combine the info collected from all sources
		
		positions = {'Genre':1,'Origin':2,'Albumsrc':3}
		genre_alternative = False
		

		# quality control
		

		#Don't bother saying 'US'
		deleteUS = INFO[2].find(', United States')
		if deleteUS > -1:
			INFO[2] = INFO[2][:deleteUS]

		return INFO

		

	def cleanGenres(self, genres, bandname): # standardize the likely spam-filled list of genres collected from all sources into a meaningful pair which will be displayed
		# remove
	#	print genres
		bannedGenres = ['Experimental', 'Other', 'Vocalist', 'Prog', 'New\sYork', 'Boston', 'Seattle', 'Canad', 'Post-', 'Irish', 'Singer[ -]Songwriter', 'Ambient'] # "All music is experimental." - Partick Leonard
		toRemove = []
		for genre in genres:
			for ban in bannedGenres:
				if re.search(ban, genre, re.I):
					toRemove.append(genre) # this proxy is required
		for genre in toRemove:
			genres.remove(genre)

		# replace and remove band's own name (sometimes on Last.fm as a tag)

		replacements = {'Jazz-rock': 'Jazz Fusion', 'Hip\shop': 'Hip-hop', 'R&amp;b':'R&B'}

		for i, n in enumerate(genres):
			for repl in replacements:
				if re.search(repl, n, re.I):
					genres[i] = replacements[repl]
			if bandname.lower() in n.lower():
				genres.remove(n)
		
		
		# capitalize

		for genre in genres:
			ind = genres.index(genre)
			genres[ind] = string.capitalize(genre.replace('&#160;', ' '))
		return genres



	def cleanGenresFinal(self, genres, wikiINFO):
		
	#	print genres

		workingList = []

		overlaps = []

		# get rid of redundancy, choose more descriptive phrases over lesser ones


		wordDict = defaultdict(list)
		for genre in genres:
			genre_lower = genre.lower()
			for word in genre_lower.split():
				wordDict[word.lower()].append(genre)
		for word, occurrences in wordDict.iteritems():
			if len(occurrences) > 1:
				overlaps += occurrences				
			#	print word, occurrences
				remove = []
		
		rest = list(set(genres).difference(set(overlaps)))
		
		for genre in overlaps:
			if overlaps.count(genre) > 1:
				overlaps.remove(genre)

		print 'working', workingList, 'rest', rest, 'overlaps', overlaps

		
		

		
		done = False # we're just beginning!

		# stage 1
		if len(rest) == 0 and len(overlaps) != 0: # all the genres gathered are similar & probably redundant; use only the shortest one
			workingList.append(min(overlaps, key=len))
			done = True
		
		if not done:
			if len(overlaps) != 0:
				workingList.append(overlaps.pop(0))

			if len(rest) != 0:
				workingList.append(rest.pop(0))
			
			if len(workingList) == 2:
				done = True
			else:
				source = max([overlaps, rest], key=len)
				try:
					workingList.append(source[int(len(source)/2)])
				except:
					pass




								
		return workingList

	def cleanOrigin(self, origin):
		nickname = False
		majorCities = {'Seattle': 'Seattle', 'Boston': 'Boston', 'New York, New York': 'NYC', 'Los Angeles': 'LA', 'Portland': 'Portland'}
		states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']
		postalCodes = {'WA': 'Washington', 'DE': 'Delaware', 'WI': 'Wisconsin', 'WV': 'West Virginia', 'HI': 'Hawaii', 'FL': 'Florida', 'WY': 'Wyoming', 'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico', 'TX': 'Texas', 'LA': 'Louisiana', 'NC': 'North Carolina', 'ND': 'North Dakota', 'NE': 'Nebraska', 'TN': 'Tennessee', 'NY': 'New York', 'PA': 'Pennsylvania', 'CA': 'California', 'NV': 'Nevada', 'VA': 'Virginia', 'CO': 'Colorado', 'AK': 'Alaska', 'AL': 'Alabama', 'AR': 'Arkansas', 'VT': 'Vermont', 'IL': 'Illinois', 'GA': 'Georgia', 'IN': 'Indiana', 'IA': 'Iowa', 'OK': 'Oklahoma', 'AZ': 'Arizona', 'ID': 'Idaho', 'CT': 'Connecticut', 'ME': 'Maine', 'MD': 'Maryland', 'MA': 'Massachusetts', 'OH': 'Ohio', 'UT': 'Utah', 'MO': 'Missouri', 'MN': 'Minnesota', 'MI': 'Michigan', 'RI': 'Rhode Island', 'KS': 'Kansas', 'MT': 'Montana', 'MS': 'Mississippi', 'SC': 'South Carolina', 'KY': 'Kentucky', 'OR': 'Oregon', 'SD': 'South Dakota'}

		# don't both specifying states of major cities
		
		for city in majorCities:
			if city in origin:
				origin = majorCities[city]
				nickname = True

		# change postal abbreviation to full state name	
		if not nickname:
			for code in postalCodes:
				if code in origin:
					origin = origin.replace(code, postalCodes[code])

			# cut off after state name

			for state in states:
				if state.lower() in origin.lower():
					origin = origin[:origin.lower().index(state.lower()) + len(state)]
			
			# remove regions, western, eastern, etc

			for region in ['western', 'eastern', 'northern', 'southern']:
				r = re.search(region + '\s', origin, re.I)
				if r:
					origin = origin.replace(r.group(0), '')


			origin = origin.split(', ')
			
			for index,word in enumerate(origin):
				origin[index] = string.capitalize(word)
			origin = ', '.join(origin)

			origin = origin.split(' ')
			
			for index,word in enumerate(origin):
				origin[index] = string.capitalize(word)
			origin = ' '.join(origin)


		return origin

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
		From = 'scapebot'
		smtpPass = open('smtppass.txt').readline()[0:9]
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
