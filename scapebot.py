' scapebot is a part of Carl Sagans Laboratories '
' authored by Artur Sapek '





from BeautifulSoup import BeautifulSoup, SoupStrainer
from mechanize import Browser
from collections import defaultdict
import csv
import string
import re
import os
#from PIL import Image




class scapebot():

    def __init__(self):
        global months 
        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        global monthsabbr 
        monthsabbr = ['Jan', 'Feb', 'Mar', 'April', 'May', 'June', 'July', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        global unicode_to_text_Matches
        unicode_to_text_Matches = { 161: '!', 192: 'A', 193: 'A', 194: 'A', 195: 'A', 196: 'A', 197: 'A', 198: 'Ae', 199: 'C', 200: 'E', 201: 'E', 202: 'E', 203: 'E', 204: 'I', 205: 'I', 
                                    206: 'I', 207: 'I', 208: 'Th', 209: 'N', 210: 'O', 211: 'O', 212: 'O', 213: 'O', 214: 'O', 216: 'O', 217: 'U', 218: 'U', 219: 'U', 220: 'U', 221: 'Y', 222: 'th', 223: 'ss', 224: 'a', 
                                    225: 'a', 226: 'a', 227: 'a', 228: 'a', 229: 'a', 230: 'ae', 231: 'c', 232: 'e', 233: 'e', 234: 'e', 235: 'e', 236: 'i', 237: 'i', 238: 'i', 239: 'i', 240: 'th', 241: 'n', 242: 'o', 
                                    243: 'o', 244: 'o', 245: 'o', 246: 'o', 248: 'o', 249: 'u', 250: 'u', 251: 'u', 252: 'u', 253: 'y', 254: 'th', 255: 'y' }
        global text_to_unicode_Matches
        text_to_unicode_Matches = { '!': [161], 'A': [192, 193, 194, 195, 196, 197], 'C': [199], 'E': [200, 201, 202, 203], 'I': [204, 205, 206, 207], 'O': [210, 211, 212, 213, 214, 216], 
                                    'N': [209], 'U': [217, 218, 219, 220], 'Y': [221], 'e': [232, 233, 234, 235], 'a': [224, 225, 226, 227, 228, 229], 'c': [231],  
                                    'i': [236, 237, 238, 239], 'o': [242, 243, 244, 245, 246, 248], 'n': [241], 'ss': [223], 'u': [249, 250, 251, 252], 'y': [253, 255] }
        global states
        states = [  'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 
                    'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 
                    'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington',
                    'West Virginia', 'Wisconsin', 'Wyoming' ]

    def sanitize(self, x): #clean up names which are often not spelled consistently
        for i in range(1, 32):
            x = ''.join(x.split(str(string.punctuation)[i]))
        return x
        
    def command(self):    # Commandline interpreter
        userinput = raw_input('> ')
        self.Comet_Tavern(userinput)

    def stripofASCII(self, string):
        pass

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
            #   print show
                writer.writerow(tuple(show))
            
        file.close()

    def researchLoop(self):
        nameInput = raw_input('> ')
        local = raw_input('local? ')
        try:    
            if nameInput != 'exit':
                if local == 'y': L = True
                else: L = False
                try:
                    print self.researchBand(nameInput, L)
                except:
                    print 'Crashed; not found'
                self.researchLoop()
            else:
                pass
        except:
            pass
        

    


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
    
    
    # Googles something, returns the results as BeautifulSoup

    def Google(self, query, ignoreSuggest):
        br = Browser()
        br.set_handle_robots(False)
        br.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.202 Safari/535.1')]                       
        br.open('http://google.com')
        br.select_form(nr=0)
        if len(query) / len(query.split()) <= 3:
            query = '"%s"' % query
            wuLyfCoefficient = False
        else:
            query = '%s' % query
            wuLyfCoefficient = True
        br['q'] = query
        soup = BeautifulSoup(br.submit().read())
        if ignoreSuggest:
            suggestLink = soup.find('a', attrs={ 'class' : 'spell_orig' })
            if suggestLink: soup = BeautifulSoup(br.follow_link(text=suggestLink.renderContents()).read()) # be stubborn and ignore Google's suggestion
        try: 
            results = soup.find('ol', attrs={ 'id': 'rso' })
        except:
            results = ''
        return results

    def GoogleSuggest(self, query):
        br = Browser()
        br.set_handle_robots(False)
        br.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.202 Safari/535.1')]                       
        br.open('http://google.com')
        br.select_form(nr=0)
        if len(query) / len(query.split()) <= 3:
            query = '"%s"' % query
            wuLyfCoefficient = False
        else:
            query = '%s' % query
            wuLyfCoefficient = True
        br['q'] = query
        soup = BeautifulSoup(br.submit().read())
        try: 
            suggestion = soup.findAll('p', attrs={ 'class' : 'sp_cnt' })[0].a
            for i in suggestion('i'):
                i.replaceWith(i.renderContents())
            for b in suggestion('b'):
                b.replaceWith(b.renderContents())
            suggestion = suggestion.renderContents().replace('"', '').replace('- ', '-').replace('&quot', '').replace(';', '')
        except:
            suggestion = None
        return suggestion


    # band names are so difficult :(

    def regexifyBandname(self, bandname):
        # regexes for flexibility when checking a page for actual mentions of the name ^_^
        change = { 'the ': '(the\s)?', ' ':'[-\s,]?', ' & ':'\sand\s|\s&\s',' and ':'\sand\s|\s&\s','DJ ':'(DJ\s)?','dj ':'(dj\s)?',}
        for c in change:
            bandname = bandname.replace(c, change[c])
        r = u''
        for i in bandname: # take care of unicode chars. shitty metal bands often use special characters to look hardcore
            if unicode_to_text_Matches.has_key(ord(i)):
                r += '[' + unicode_to_text_Matches[ord(i)] + i + ']'
            if text_to_unicode_Matches.has_key(i):
                r += '[' + i 
                for val in text_to_unicode_Matches[i]:
                    r += unichr( val )
                r += ']'
            elif ord(i) >= 0x80:
                pass
            else:
                r += i
        return r
    
    def bandAlreadyScraped(self, bandname):
        db = open('bandsScraped.txt', 'rb')
        lines = db.readlines()
        if bandname not in lines:
            db.close()
            db = open('bandsScraped.txt', 'a')
            db.write('\n' + bandname)
            db.close()
            x = False
        else:
            x = True
        return x






    def research(self, bandname, ignoreS = False, local = False):
        try:
            print self.researchBand(bandname, local, ignoreS)
        except:
            pass






    # keeps a db of legit genres from Wikipedia and Last.fm, and a count of their appearance, to pick out realistic ones from bandcamp/myspace/other user-edited sources
    def genresDB(self, genres, bandname):
        if not self.bandAlreadyScraped(bandname):
            toAdd = []
            db = open('genres.csv', 'rb')
            temp = open('temp.csv', 'wb')
            reader = csv.reader(db)
            writer = csv.writer(temp)
            db.seek(0)
            for line in reader:
                if line[0] in genres:
                    writer.writerow((line[0], str(int(line[1]) + 1)))
                    genres.remove(line[0])
                else:
                    writer.writerow(line)
            for genre in genres:
                writer.writerow((genre, 1))
            db.close()
            temp.close()
            with open('temp.csv', 'rb') as temp:
                lines = temp.readlines()
                lines.sort()
            with open('genres.csv', 'wb') as genres:
                genres.writelines(lines)
            temp.close()
            genres.close()
            os.remove('temp.csv')


        

    # huge function: researchBand
    # input: band name
    # output: [band name formatted, [one or two genres], band's origin (city/state), album cover source local]
    # called in scraping function for each band in show that's not already in db

    def researchBand(self, bandname, forceLocal = False, ignoreSuggest = False):
        # set some quality-assurance variables :) <3
        nameFormatted = False
        GENRES = []
        TRUSTWORTHY_GENRES = []
        results = ''
        sources = {}
        newestAlbumName = alternate = None
        originalInput = bandname
        wikiINFO = lastfmINFO = soundcloudINFO = bandcampINFO = facebookINFO = myspaceINFO = reverbnationINFO = {}
        soupREPO = {}
        
        # yes I'm a bastard

        br = Browser()
        br.set_handle_robots(False)
        br.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.202 Safari/535.1')]   

        # see if Google thinks the name is misspelled


        suggestion = self.GoogleSuggest(bandname)

        # R E C U R S I O N ~~~~~ *****
        if not ignoreSuggest:
            if suggestion: # so, here we have two possibilities: the venue made a typo, or the band picked a similar name to a more popular band. 
                           # let's try giving the venue the benefit of the doubt and rerun with ignore set to False
                alternate = self.researchBand(bandname, forceLocal, ignoreSuggest = True)
                          
        # ok now that that shit is figured out, let's continue with the fixed band name
        # be more specific with search when dealing with Myspace and Wiki - they're not musician-specific

        if alternate:
            print 'fuck all!'
            return alternate
        if not ignoreSuggest:
            if suggestion:
                x = len(bandname.split())
                bandname = ' '.join(suggestion.split()[0:x])


        query = bandname
        if forceLocal: query += ' Seattle'


        myspaceMusic_results = self.Google('%s music myspace' % query, ignoreSuggest)
        for li in myspaceMusic_results('li'):
            try:
                link = li.div.h3.a
                if re.search('myspace.com', link['href']):
                    m = re.match('http://www.myspace.com/[^/]*', link['href'])
                    if m:
                        URL = str(m.group(0))
                    soup = BeautifulSoup(br.open(URL).read())
                    if re.search(self.regexifyBandname(bandname), str(soup), re.I) and len(soup.findAll('h3', text='General Info', attrs={ 'class' : 'moduleHead' })) > 0:
                        sources['Myspace'] = URL
                        soupREPO['Myspace'] = soup
                        break
            except:
                pass

        # find Wikipedia

        wiki_results = self.Google('%s music wikipedia' % bandname, ignoreSuggest)
        for li in wiki_results('li'):
            try:
                link = li.div.h3.a
                if re.search('wikipedia.org', link['href']):
                    soup = BeautifulSoup(br.open(link['href']).read())
                    header = soup.h1.renderContents()
                    if header.find('song)') == -1 and re.search(self.regexifyBandname(bandname), str(soup), flags=re.I) and len(soup.findAll('a', href='/wiki/Music_genre')) > 0 and re.search(self.regexifyBandname(bandname), soup.h1.renderContents(), re.I) and '(soundtrack)' not in soup.h1.renderContents() and 'album)' not in soup.h1.renderContents():
                        sources['Wikipedia'] = str(link['href'])
                        soupREPO['Wikipedia'] = soup                        
                        break
            except:
                pass

        # search for bandcamp

        bandcamp_results = self.Google('%s bandcamp' % query, ignoreSuggest)
        for li in bandcamp_results('li'):
            try:
                link = li.div.h3.a
                URL = link['href']
                m = re.search('bandcamp.com', URL) # this extra step makes sure we don't end up with the root URL of someone who mentions the bandname in a song title or some shit
                if m:
                    URL = str(URL[:URL.find(m.group(0)) + 12])
                    soup = BeautifulSoup(br.open(URL).read())
                    # from here down, it makes sure we haven't found the bandcamp or an artist with a similar name to a  mainstream artist without a bandcamp. an example I've found is 'beck burger' for 'beck'
                    # also for safe measure is the '[^\w]' part of the regex in case it were 'beckburger': no compound words containing the name we're looking for
                    byline = soup.findAll('span', attrs={'itemprop': 'byArtist'})[0]
                    for a in byline('a'):
                        a.replaceWith(a.renderContents())

                    bl = str(byline.renderContents()).replace('\n', '').strip()
                    r = re.search(self.regexifyBandname(bandname), bl, flags=re.I)
                    bl = bl[bl.find(r.group(0)):].split()
                    if r and len(bandname.split()) == len(bl): # checks for other words or compound words
                        sources['Bandcamp'] = URL
                        soupREPO['Bandcamp'] = soup                        
                        break
            except:
                pass



        results = self.Google(query, ignoreSuggest)


        for li in results('li'):
            try:
                for em in li(['em', 'b']):
                    em.replaceWith(em.renderContents())
                #print li.div.h3.a.renderContents(), li.div.h3.a['href']

                #print li.a.renderContents() 
                link = li.div.h3.a
                #print link.renderContents()
                knownSources = {'Last.fm': 'last.fm/music', 'Soundcloud': 'soundcloud.com', 'ReverbNation': 'reverbnation.com', 'Facebook': 'facebook.com'}
                for entry in knownSources:
                    try:
                        temp = link['href'].index(knownSources[entry])
                        #so it doesn't redefine entries with lower results:
                        if entry in sources:
                            break
                        try:
                            #print '.', knownSources[entry], self.sanitize(bandname) 
                            #print link['href']
                            URL = link['href']
                            if entry == 'Last.fm': # make sure to go to the artist's root page and not videos or something
                                m = re.match('http://www.last.fm/music/[^/]*', sources[entry])
                                if m:
                                    URL = m.group(0)

                            soup = BeautifulSoup(br.open(URL).read())
                            
                            if re.search(self.regexifyBandname(bandname), str(soup), re.I):
                                URL = re.match('[^?]*', str(link['href'])).group(0)
                                sources[entry] = URL
                                soupREPO[entry] = soup
                            break
                        except:
                            pass
                    except:
                        pass
            except:
                pass


        print sources
    
        # need to append genre, origin, and album cover

            
        if 'Wikipedia' in sources:
            #scrape wikipedia
            wikiINFO = {}
            soup = soupREPO['Wikipedia']
        #   print 'wiki'

            try:
                #redefine bandname with formatting from wiki header, band names can be weird, number 1 trusted source for name formatting
                possibleName = soup.h1.renderContents().replace(' (musician)', '').replace(' (band)', '').replace(' (rock band)', '').replace('User:', '').replace(' (singer)', '')
                if possibleName.find('<i>') > -1:
                    nameFormatted = False
                else:
                    bandname = possibleName
                    nameFormatted = True # name formatting done, that was easy :)
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
                for span in genreInfo('span'):
                    span.replaceWith(span.renderContents())
                genres = genreInfo.renderContents().split(', ')
                

                
                # dealing with newlines:

                if genres[0].find('\n') > -1 and len(genres) == 1:
                    genres = re.sub('\n', ', ', genres[0]).split(', ')

                    
                genres = self.cleanGenres(genres, bandname)

                
                wikiINFO['Genre'] = genres  
                
                GENRES += genres
                TRUSTWORTHY_GENRES += genres

            #   print 'WIKI genres', genres
                
            except:
                pass
            # genres done, now try to get the name of the most recent album
            # wikipedia is mad inconsistent with how they list albums. fuckall. this might be difficult, I'll come back later
            
            # Find Newest Album
            # still a lot of work to do on this

            ALBUMSLIST = None
            ALBUMSTABLE = None
    
            # if there's a link to the discography follow it
            try:
                soup = BeautifulSoup(br.follow_link(text_regex=r'.*discography', nr=0).read())
            except:
                pass

            try:
                for t in soup.findAll('table'):
                    try:
                        if re.search('detail|title', t.findAll('th')[1].renderContents(), re.I):
                            ALBUMSTABLE = t
                            break
                    except:
                        pass
                if ALBUMSTABLE != None:
                    rows = ALBUMSTABLE.findAll('tr')
                    goUp = 1
                    target = rows[len(rows) - goUp]                         
                    while re.search('denotes releases that did not chart', target.renderContents(), re.I) or re.search('to be released|2012', target.renderContents(), re.I):
                        goUp += 1
                        target = rows[len(rows) - goUp]                         
                    target = target.i
                    for a in target('a'):
                        a.replaceWith(a.renderContents())
                    for b in target('b'):
                        b.replaceWith(b.renderContents())
                    target = target.renderContents()
                    newestAlbumName = target
                            
                
                # or it could be 
                if not newestAlbumName:
                    discog = soup.findAll('span', attrs={ 'class' : 'mw-headline'})             
                    for i, n in enumerate(discog):
                        if re.search('album', n.renderContents(), re.I):
                            ALBUMSLIST = n.parent.nextSibling.nextSibling.findAll('li')
                            newest = ALBUMSLIST[len(ALBUMSLIST) - 1]
                            if newest.i:
                                if newest.i.a: newestAlbumName = newest.i.a.renderContents()
                                else: newestAlbumName = newest.i.renderContents()
                if newestAlbumName != 'None':
                    pass#print newestAlbumName           
            except:
                pass

        if 'Last.fm' in sources:

            try:
                #scrape last.fm
                lastfmINFO = {}
                soup = soupREPO['Last.fm']
            #   print 'last.fm'
                try:
                    soup = str(soup)
                    genreMeta = soup.index('itemprop="keywords"') # this is a hack, cos for some reason BeauSoup doesnt find itemprop attrs
                    genres = soup[genreMeta + 29:]
                    genres = genres[:genres.index('">')]
                    genres = genres.split(', ')
                    toRemove = []
                    for genre in genres:
                        try:
                            genreSoup = br.open('http://last.fm/tag/' + genre.replace(' ', '%20')).read() # only keeps legit genres with tag pages
                            if re.search('a description for this tag yet', genreSoup):
                                toRemove.append(genre)
                        except:
                            pass
                    for genre in toRemove:
                        genres.remove(genre)
                    
                    if not nameFormatted:
                        nameMeta = soup.index('itemprop="name"')
                        bandname = soup[nameMeta + 16:]
                        bandname = bandname[:bandname.index('</h1>')]
                    #   print 'name reformatted from last.fm'
                        nameFormatted = True
                        
                    # sometimes last.fm will have a band/musician's own name as a tag
                    genres = self.cleanGenres(genres, bandname)

                    GENRES += genres                    

                    TRUSTWORTHY_GENRES += genres
                        
    
                    
                    
                except:
                    pass
                
                # origin
                
                try:
                #   print 'origin from lastfm'
                    soup = str(soup)
                    localityInd = soup.index('p class="origin"') # also a hack, fuckall
                    locality = soup[localityInd:]
                    locality = locality[locality.find('<strong>') + 8:]
                    locality = locality[:locality.index('\n')]
                    locality = BeautifulSoup(locality)
                    for span in locality('span'):
                        span.replaceWith(span.renderContents())
                    locality = str(locality)
                #   print 'last.fm origin: ', locality
                        
                except:
                    pass

            #   print 'LAST.FM genres', genres

                lastfmINFO['Genre'] = genres
                if locality != '</strong>':
                    lastfmINFO['Origin'] = locality


            except:
                pass
        


        if 'Soundcloud' in sources:
            #scrape soundcloud
            
            # genres
            
            soundcloudINFO = {'Genres': []}
            soup = soupREPO['Soundcloud']

            target = soup.findAll('span', { 'class' : 'genre' })
            for genre in target:
                if genre.renderContents() not in soundcloudINFO['Genres']:
                    soundcloudINFO['Genres'].append(genre.renderContents())
            soundcloudINFO['Genres'] = self.cleanGenres(soundcloudINFO['Genres'], bandname)

            GENRES += soundcloudINFO['Genres']
            
            # name (if no Wiki which is likely for bands with soundclouds)
            try:
                if len(tags) > 0:
                    temp = soup.findAll('div', attrs={ 'id' : 'user-info'})[0]
                    if not nameFormatted:
                        bandname = temp.h1.renderContents()[:temp.h1.renderContents().find('\n')]
                        nameFormatted = True
                        origin = temp.span.renderContents()
                        soundcloudINFO['Origin'] = origin
            except:
                pass

        

        if 'Myspace' in sources:
        #   print 'myspace'
            myspaceINFO = {}
            soup =  soupREPO['Myspace']

            # myspace is not valid for formatting the bandname, for no good reason they are often in all-caps
            try:    
                target = soup.findAll(attrs={'class':'odd BandGenres'})[0]
                for tag in target.findAll(True):
                    tag.replaceWith(tag.renderContents())
                target = target.renderContents()[8:]
                genres = self.cleanGenres(target.split(' / '), bandname)

                TRUSTWORTHY_GENRES += genres

            #   print 'MYSPACE genres', genres
                GENRES += genres
                myspaceINFO['Genres'] = genres
                target = soup.findAll(attrs={'class':'even Location'})[0]
                for span in target('span'):
                    span.replaceWith(span.renderContents())
                for strong in target('strong'):
                    strong.replaceWith(strong.renderContents())
                myspaceINFO['Origin'] = target.renderContents()[10:].strip()            

            except:
                pass

        if 'ReverbNation' in sources:
            reverbnationINFO = {}
            soup = soupREPO['ReverbNation']

            # so reverb nation all-capses all artist names for some fucking reason. if this is the only source we'll just string.capwords it get genres and origin tho
            info = soup.findAll('div', attrs={ 'class' : 'location_genres' })[0].renderContents() # all we need
            parts = info.split('\n')
            reverbnationINFO['Origin'] = parts[1].strip().replace('\r', '')
            reverbnationINFO['Genres'] = parts[3].strip().replace('\r', '').split(' / ')
            GENRES += reverbnationINFO['Genres']
        

        if 'Facebook' in sources:
            facebookINFO = {}
            soup = soupREPO['Facebook']

            # BeautifulSoup isn't of much use here because the code Facebook compiles into looks like shit
            ht = soup.find('Hometown</th>')
            if ht > -1: 
                origin = soup[ht + 54:]
                origin = origin[:origin.find('</')]
                facebookINFO['Origin'] = origin
            ge = soup.find('Genre</th>')
            if ge > -1: 
                genre = soup[ge + 51:]
                genre = genre[:genre.find('</')]
                GENRES.append(genre)


                

        if 'Bandcamp' in sources:
            temp = []
            tagsFound = None
            bandcampINFO = {}
            soup = soupREPO['Bandcamp']
            tags = soup.findAll('dd', attrs={ 'class' : 'tralbumData' })
            if len(tags) > 0:
                for tagsPossible in tags:
                    if 'tags:' in tagsPossible.renderContents():
                        tagsFound = tagsPossible
                        break
                if tagsFound:
                    for a in tagsFound('a'):
                        temp.append(a.renderContents())
                    x = 1
                    if temp[len(temp) - 1].split(' ')[0][0].isupper():
                        bandcampINFO['Origin'] = temp[len(temp) - 1]
                        x = 2
                    bandcampINFO['Genres'] = temp[:len(temp) - x]
                    GENRES += self.cleanGenres(bandcampINFO['Genres'], bandname)
                    # if we get bandcamp its often going to be the only source so let's milk it
                    if not nameFormatted:
                        namesection = soup.findAll('dl', attrs={ 'id' : 'name-section' })[0]
                        artistname = namesection.span
                        for a in artistname('a'):
                            a.replaceWith(a.renderContents())
                        bandname = artistname.renderContents().split()
                        # if all lowercase it's prob. negligence; capitalize. if any letters capital, then theyve formatted it and we'll leave it how it is. ex: avi buffalo => Avi Buffalo; tUnE-yArDs, Earl Sweatshirt, IDOLS left alone
                        changeIt = True
                        for index, word in enumerate(bandname):
                            if not changeIt: break
                            for char in word:
                                if char.isupper():
                                    changeIt = False
                                    break
                        if changeIt:
                            for index, word in enumerate(bandname):
                                bandname[index] = string.capitalize(word)
                        bandname = ' '.join(bandname)
                        nameFormatted = True
                        
            
            
        if not nameFormatted: # if we haven't found out how to format the name, default to proper grammar
            bandname = string.capwords(bandname)
            bandname = bandname.split('-')
            for index, word in enumerate(bandname):
                if len(word.split()) == 1:
                    bandname[index] = string.capwords(word)
            bandname = '-'.join(bandname)
            nameFormatted = True

        INFO = [self.cleanBandname(bandname, originalInput),'','','']

        for genre in GENRES:
            if GENRES.count(genre) > 1:
                GENRES.remove(genre)

        INFO[1] = self.chooseGenres(GENRES)

        originSrcs = [wikiINFO, lastfmINFO, soundcloudINFO, bandcampINFO, facebookINFO, reverbnationINFO, myspaceINFO]
        for src in originSrcs:
            if INFO[2] == '' and 'Origin' in src:
                INFO[2] = self.cleanOrigin(src['Origin'], bandname)
            else:
                pass




                
    
        # combine the info collected from all sources
        
        positions = {'Genre':1,'Origin':2,'Albumsrc':3}
        genre_alternative = False
        
        t_g = TRUSTWORTHY_GENRES

        

        toRemove = []

        if len(TRUSTWORTHY_GENRES) > 0:
            t_g.sort()
            for ind, genre in enumerate(t_g):
                if t_g[ind - 1] == genre:
                    toRemove.append(genre)
        
        for genre in toRemove:
            t_g.remove(genre)
        
        self.genresDB(t_g, bandname)




        # quality control
        
        INFO[0] = INFO[0].strip()
        
        INFO[2] = INFO[2].strip()
        
        
        #Don't bother saying 'US'
        
        
        # return if we have something

        if len(INFO[1]) != 0:
            return INFO
        else:
            return None












    def cleanBandname(self, name, original):
        alternatives = name.split('/') # there's been an instance where wikipedia gives an old name/new name combo. in this case just go with what they're going by now
        if len(alternatives) > 1:
            for piece in alternatives:
                if re.search(original, piece, re.I):
                    name = string.capitalize(piece)
        return name.replace('&amp;', '&')

    def cleanGenres(self, genres, bandname): # standardize the likely spam-filled list of genres collected from all sources into a meaningful pair which will be displayed on the page
        bannedGenres = ['Experimental', 'Other', 'Vocalist', 'Prog', 'Hard Rock' ,'New\sYork', 'Boston', 'Seattle', 'Canad', 'Post[ -]', 'Singer[ -]Songwriter', 
                        'Ambient', 'Underground', 'Scotland', 'ish', 'Freestyle', 'Good music', 'Regional mexican', 'Chicago', 'Swag', 'Denton', 'Communication', 
                        'Minimalist', 'Australian', '80', '70', 'Music', 'Song'] # "All music is experimental." - Partick Leonard
        bannedGenres += states
        toRemove = []

        # remove any HTML tags that may have made it through
        for ind, genre in enumerate(genres):
            genre = BeautifulSoup(genre)
            for tag in genre(True):
                tag.replaceWith(tag.renderContents())
            genres[ind] = str(genre)


        # remove bad genres
        for genre in genres:
            for ban in bannedGenres:
                if re.search(ban, genre, re.I) or genre == '':
                    toRemove.append(genre) # this proxy is required as Zorah exhibited in her Google interview
        for genre in toRemove:
            genres.remove(genre)
        
        rewords = {'Jazz-rock': 'Jazz Fusion', 'R[&amp;|n|&]b':'R&B', 'Desert rock': 'Stoner rock', 'Classic Rock': 'Rock',
                   'Rock and Roll': 'Rock n Roll', 'Rock \'n\' Roll': 'Rock n Roll'} # attention to detail is the most important part

        for i, n in enumerate(genres):
            for repl in rewords:
                if re.search(repl, n, re.I):
                    genres[i] = rewords[repl]
            if bandname.lower() in n.lower() or len(n.split()) > 3: # second part dubbed the Gorge Mand rule, thank you Alina. "tags: [...], Kreayshawn can suck my clit, [...]"
                genres.remove(n)
        
        replacements = {'West coast\s?': '', 'East coast\s?': '', 'Alternative\s': 'Alt. ', ' revival': '', ' hop': '-hop', 'phop': 'p-hop'}
        for i, n in enumerate(genres):
            for repl in replacements:
                r = re.search(repl, n, re.I)
                if r:
                    # print r.group(0)
                    genres[i] = genres[i].replace(r.group(0), replacements[repl])

        
        # capitalize
        for genre in genres:
            if genre not in rewords.itervalues():
                ind = genres.index(genre)
                genres[ind] = string.capitalize(genre.replace('&#160;', ' '))

        return genres


    
    def chooseGenres(self, genres):
        workingList = []
        overlaps = []
        done = False

        lastResorts = ['Electronic', 'Electronica', 'Indie', 'Rock', 'Alternative'] # prefer to remove genres that don't really mean shit but they can be a last resort. this usually leads scapebot to pick more interesting genres :)
        remove = []
        for i, n in enumerate(genres):      
            for resort in lastResorts:
                if n == resort:
                    if n not in remove: # sometimes it adds in dupes without this
                        remove.append(n)

        for rem in remove:
            if len(genres) > 1:
                genres.remove(rem)



        # stage 0: get rid of redundancy, choose more descriptive/unique phrases over lesser ones
        wordDict = defaultdict(list)
        for genre in genres:
            for word in genre.split():
                wordDict[word.lower()].append(genre)
        for word, occurrences in wordDict.iteritems():
            if len(occurrences) > 1:
                overlaps += occurrences             
            #   print word, occurrences
        
        rest = list(set(genres).difference(set(overlaps)))
        
        for genre in overlaps:
            if overlaps.count(genre) > 1:
                overlaps.remove(genre)

        #print 'rest', rest, 'overlaps', overlaps
        

        # stage 1: 
        if overlaps:
            best = max(overlaps, key=lambda x: len(x) / len(x.split()))
        if len(rest) == 0 and len(overlaps) != 0: # all the genres gathered are similar so we have to be careful not to be redundant
            workingList.append(best)
            overlaps.remove(best)
            firstGenre = workingList[0]
            for genre in overlaps:
                match = False
                for word in genre.split():
                    if re.search(word, firstGenre, re.I):
                        match = True
                        overlaps.remove(genre)
                        break
                if not match and not done:
                    workingList.append(genre)
                    done = True
                    break
        # stage 2: we have shit to work with so let's work with it
        if not done:
            if rest:
                workingList.append(rest.pop(0))
                if overlaps:
                    workingList.append(best)
                elif rest:
                    workingList.append(rest.pop(0))
                else:
                    pass
            
            

        # replacements that wont fuck with how things are chosen
        finalReplacements = {'Alt-':'Alt. ','&amp;':'&'}
        for i, n in enumerate(workingList):
            for repl in finalReplacements:
                if repl in n:
                    workingList[i] = workingList[i].replace(repl, finalReplacements[repl])


        if len(workingList) == 2:
            workingList = ' / '.join(workingList).strip()
        elif workingList:
            workingList = workingList[0]
        else:
            workingList = ''
        return workingList




    # Standardize the formatting and verunacular in the origin field. City and state if city is not famous, no postal codes or 'United States'
    def cleanOrigin(self, origin, bandname):
 
         # For keeping track of shit
        nickname = False

        # Call these cities just by their name or nickname, everyone knows them
        majorCities = { 'Seattle|Seatle|Seatttle': 'Seattle', 'Boston': 'Boston', 'Los Angeles': 'LA', 'Portland': 'Portland', 'Providence': 'Providence', 'Long Beach, California': 'Long Beach', 'San Fransisco': 
                        'San Fransisco', 'Berkeley': 'Berkeley', 'Brooklyn': 'Brooklyn', 'Long Island': 'Long Island', 'Minneapolis': 'Minneapolis', 'Coney Island': 'Coney Island', 'Vancouver, BC': 'Vancouver, BC'}
        
        # No postal codes!
        states = { 'Mississippi': 'MS', 'Oklahoma': 'OK', 'Wyoming': 'WY', 'Minnesota': 'MN', 'Alaska': 'AK', 'Illinois': 'IL', 'Arkansas': 'AR', 'New Mexico': 'NM', 'Indiana': 'IN', 'Maryland': 'MD', 
                    'Louisiana': 'LA', 'Texas': 'TX', 'Iowa': 'IA', 'Wisconsin': 'WI', 'Arizona': 'AZ', 'Michigan': 'MI', 'Kansas': 'KS', 'Utah': 'UT', 'Virginia': 'VA', 'Oregon': 'OR', 'Connecticut': 'CT', 
                    'Tennessee': 'TN', 'New Hampshire': 'NH', 'Idaho': 'ID', 'West Virginia': 'WV', 'South Carolina': 'SC', 'California': 'CA', 'Massachusetts': 'MA', 'Vermont': 'VT', 'Georgia': 'GA', 
                    'North Dakota': 'ND', 'Pennsylvania': 'PA', 'Florida': 'FL', 'Hawaii': 'HI', 'Kentucky': 'KY', 'Rhode Island': 'RI', 'Nebraska': 'NE', 'Missouri': 'MO', 'Ohio': 'OH', 'Alabama': 'AL', 
                    'South Dakota': 'SD', 'Colorado': 'CO', 'New Jersey': 'NJ', 'Washington': 'WA', 'North Carolina': 'NC', 'New York': 'NY', 'Montana': 'MT', 'Nevada': 'NV', 'Delaware': 'DE', 'Maine': 'ME' }

        stateInd = -1

        if origin.find(', ') == -1:
            origin = origin.replace(' ', ', ')

        origin = origin.split(', ')

        toRemove = []

        for i, p in enumerate(origin):
            s = string.capitalize(p.strip()) 
            if s in states and i > 0:
                origin[i] = states[s]
                stateInd = i
            if s.upper() in states.itervalues() and i > 0:
                stateInd = i


        if toRemove: origin.remove(toRemove[0])


        if stateInd > 0:
            for i in range(stateInd + 1, len(origin) - 1):
                origin.pop(i)
        
        origin[stateInd] = origin[stateInd].upper()


        origin = ', '.join(origin)
        
    

        # Don't both specifying states of major cities
        for city in majorCities:
            if re.search(city, origin, re.I):
                origin = majorCities[city]
                nickname = True

        # Change postal abbreviation to full state name 
        if not nickname:
        
            # Remove regions, western, eastern, etc
            for region in ['western', 'eastern', 'northern', 'southern']:
                r = re.search(region + '\s', origin, re.I)
                if r:
                    origin = origin.replace(r.group(0), '')

            regexbandname = '\s\s?'.join(bandname.split(' ')) + '[^w]\s?'  # Make sure they didnt repeat their name in their location for some stupid reason

            temp = re.search(regexbandname, origin, re.I)
            if temp:
                origin = origin.replace(origin[origin.find(temp.group(0)):len(temp.group(0))], '')
            
            origin = origin.split(', ')
            for index,word in enumerate(origin):
                if index != stateInd:
                    origin[index] = string.capwords(word)
            origin = ', '.join(origin)
            r = re.search(',? united states', origin, re.I)
            if r: origin = origin.replace(r.group(0), '')
            r = re.search(',?\s?u.?[sn].?\s?', origin, re.I)
            if r: origin = origin.replace(r.group(0), '')
            r = re.search(', Please Select Your Region', origin, re.I)
            if r: origin = origin.replace(r.group(0), '')
                    


        return origin





    # album cover funct development on hold because PIL and _imaging library installation is pathetic


    # Album_cover function. going to be super dank. seperate from rest of researchBand
    # Testing With The Big Echo By The Morning Benders
    def getAlbumCover(self, newestAlbumName):
        sources = {}
        br = self.freeBrowser()
        if 'Wikipedia' in sources:
            # Get most recent album from there
        # Should probably also find their p4k in research, too
            pass

        # Wow, Fuck, Saving Images Is Easy
        cover = open('./covers/m/TheMorningBenders.jpg', 'wb')
        
        src = br.open_novisit('http://upload.wikimedia.org/wikipedia/en/6/6c/TheMorningBendersBigEcho.jpg').read()

        cover.write(src)

        cover.close()

        cover = Image.open('./covers/m/TheMorningBenders.jpg').resize( (80,80), Image.ANTIALIAS )
        try:
            cover.save('./covers/m/TheMorningBenders.jpg', 'JPEG')
        except:
            print 'resize save error!'


    





    def freeBrowser(self):
        br = Browser()
        br.set_handle_robots(False)
        br.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.202 Safari/535.1')]
        return br






    # Scraping functions begin here!


    # All venues have functions for A) Specific date and B) Upcoming future if their homepage is formatted that way (EX: Neumos's). The latter is for efficiency and to leave as small a footprint as possible 
    # Format: [ showID, venueID, Date, Time, Price, 21+, Bands ]

    
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




    # Reach-out functions


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
            returnTweets = []
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
                returnTweets.append(tweetContents)
            return returnTweets 

    def tweet(self, tweet):
        self.twitter(['tweet', tweet])



