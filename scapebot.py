' scapebot is a part of Carl Sagans Laboratories '
' authored by Artur Sapek '

from BeautifulSoup import BeautifulSoup
from mechanize import Browser
import urllib2

months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

class scapebot():

	def command(self):
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
						print 'Error opening link'
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
							theindex = extra.index('$')
							price = extra[theindex : len(extra)]
			show.append(bands)
			show.append('%s %s' % (month, day[0:3]))
			show.append(price)
		print show
		self.command()

