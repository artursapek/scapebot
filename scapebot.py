' scapebot is a web spider that can research bands and scrape show information from Seattle venues '
' he is basically our slave '
' authors: Artur Sapek, Michael Beswetherick '

from BeautifulSoup import BeautifulSoup
from mechanize import Browser
from collections import defaultdict
from random import *
import csv
import string
import re
import os


class scapebot():

    def __init__(self):
        global thisYear
        thisYear = '2012'
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
    
    # Googles something, returns the results as BeautifulSoup

    def Google(self, query, ignoreSuggest):
        br = self.freeBrowser()    
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
            if suggestLink: 
                soup = BeautifulSoup(br.follow_link(text = query).read()) # be stubborn and ignore Google's suggestion
        try: 
            results = soup.find('ol', attrs={ 'id': 'rso' })
        except:
            results = ''
        return results

    def GoogleSuggest(self, query):
        br = self.freeBrowser()
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


    # this just became the dankest function in this file in the world. it works beautifully though.

    def regexifyBandname(self, bandname, listIt=False):
        # regexes for flexibility when checking a page for actual mentions of the name ^_^
        questionOut = ['[', ']']
        change = { 'the ': '(the\s)?', ' ':'([-\s,]?)', ' & ':'(\sand\s|\s&\s)',' and ':'(\sand\s|\s&\s)','DJ ':'(DJ\s)?','dj ':'(dj\s)?',}
        if not listIt:
            for q in questionOut:
                bandname = bandname.replace(q, q + '?')
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
        else: # do the same shit, return as a list
            changed = []
            for i,n in enumerate(bandname):
                for ind,ch in enumerate(change):
                    if bandname[i:i + len(ch)] == ch:
                        culprit = bandname[i:i + len(ch)]
                        for duba in range(0, bandname.count(culprit)):
                            w = bandname.find(culprit) # im running out of variables
                            if w != -1:
                                bandname = bandname[:w] + change[ch] + bandname[w + 1:]
                                changed.append([w, len(change[ch])]) # commit
                        # now we have an array like this [[1, 3], [5, 6]] for the fuckin indeces in the string to keep together in the list YO! so we can iterate over them as one. fuckall.

            l = []
            skip = 0
            for ind,i in enumerate(bandname): # take care of unicode chars. shitty metal bands often use special characters to look hardcore
                r = ''
                stop = False
                if skip > 0:
                    skip -= 1
                else:
                    for y,x in enumerate(changed):
                        if ind == changed[y][0]:
                            l.append(bandname[ind:ind+changed[y][1]])
                            stop = True
                            skip = changed[y][1] - 1
                            changed.pop(y)
                    if not stop:
                        if unicode_to_text_Matches.has_key(ord(i)):
                            r +=  '[' + unicode_to_text_Matches[ord(i)] + i + ']'
                        if text_to_unicode_Matches.has_key(i):
                            r += '[' + i 
                            for val in text_to_unicode_Matches[i]:
                                r += unichr( val )
                            r +=  ']' 
                            l.append( r )
                        elif ord(i) >= 0x80:
                            pass
                        else:
                            l.append( i )
            return l            # returns as a list. ''.join() this and it's the same shit as above. super dank.

            
    # moves a pair of question marks across the name, character by character. gives some tolerance for typos. fucking dank functions.

    def flexibleComparison(self, bandname, soup=None):
        # super dank. the objective: to get a typo like "andrew james robinson" to match with "andrew james robison". a pair of question marks will be gliding across the name.
        found = False
        update = bandname
        if re.search(self.regexifyBandname(bandname), str(soup), re.I):
            found = True
        if found == False:
            l = len(bandname)
            for i in range(0, l - 3):
                name = self.regexifyBandname(bandname, listIt = True) # list it bitch
                for x in range(i, i + 2):
                    try:
                        if name[x][-1] != '?' or name[x][-2] != '?':
                            name[x] = name[x] + '?\w?' # add a question mark
                    except:
                        pass
                tolerant = ''.join(name)
                r = re.search(tolerant, str(soup), re.I)
                if r:
                    found = True
                    update = r.group(0)                    
                    break
        return found, update

    
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

    # huge function: researchBand
    # input: band name
    # output: [band name formatted, [one or two genres], band's origin (city/state), album cover source local]
    # called in scraping function for each band in show that's not already in db

    def researchBand(self, bandname, forceLocal = False, ignoreSuggest = False, sources = {}):
        # set some quality-assurance variables :) <3
        nameFormatted = False
        GENRES = []
        TRUSTWORTHY_GENRES = []
        results = ''
        newestAlbumName = alternate = None
        originalInput = bandname
        wikiINFO = lastfmINFO = soundcloudINFO = bandcampINFO = facebookINFO = myspaceINFO = reverbnationINFO = {}
        soupREPO = {}
        sources = {}

        # yes I'm a bastard

        br = self.freeBrowser()

        # see if Google thinks the name is misspelled
        query = bandname
        if forceLocal: query += ' Seattle'


        suggestion = self.GoogleSuggest(query)

        # R E C U R S I O N ~~~~~ *****
        if not ignoreSuggest:
            if suggestion: # so, here we have two possibilities: the venue made a typo, or the band picked a similar name to a more popular band. 
                           # let's try giving the venue the benefit of the doubt and rerun with ignore set to False
                alternate = self.researchBand(bandname, forceLocal, ignoreSuggest = True)
                          
        # ok now that that shit is figured out, let's continue with the fixed band name
        # be more specific with search when dealing with Myspace and Wiki - they're not musician-specific

        if alternate:
            return alternate
        if not ignoreSuggest:
            if suggestion:
                x = len(bandname.split())
                bandname = ' '.join(suggestion.split()[0:x])


      

        myspaceMusic_results = self.Google('%s music myspace' % query, ignoreSuggest)
        myspaceMusic_results_alt = self.Google('\"%s\"' % bandname, ignoreSuggest)
        myspaceMusic_results = BeautifulSoup(str(myspaceMusic_results) + str(myspaceMusic_results_alt)) # specific and unspecific. try both
        for li in myspaceMusic_results('li'):
            try:
                link = li.div.h3.a
                if re.search('myspace.com', link['href']):
                    m = re.match('http://www.myspace.com/[^/]*', link['href'])
                    if m:
                        URL = str(m.group(0))
                    soup = BeautifulSoup(br.open(URL).read())
                    header = soup.findAll('h1')[1]
                    search, update = self.flexibleComparison(bandname, header.renderContents())
                    if search and len(soup.findAll('h3', text='General Info', attrs={ 'class' : 'moduleHead' })) > 0 and soup.find(attrs={'class':'odd BandGenres'}):
                        sources['Myspace'] = URL
                        soupREPO['Myspace'] = soup
                        if update != bandname: # MAKE SURE THERE ARE EVEN GENRES FUCK MAN
                            bandname = update
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
                    search, update = self.flexibleComparison(bandname, soup)
                    if header.find('song)') == -1 and search and len(soup.findAll('a', href='/wiki/Music_genre')) > 0 and re.search(self.regexifyBandname(bandname), soup.h1.renderContents(), re.I) and '(soundtrack)' not in soup.h1.renderContents() and 'album)' not in soup.h1.renderContents():
                        sources['Wikipedia'] = str(link['href'])
                        soupREPO['Wikipedia'] = soup
                        if update != bandname:
                            bandname = update
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
                URL = URL[:URL.find('com') + 3]
                URL +=  '/releases' # tack on releases to jump straight to the page that has info. this always works, it's like bandcamp did this just for me :)
                try:
                    soup = BeautifulSoup(br.open(URL).read())
                    if m or str(soup).count('bandcamp.com') > 5:
                        # from here down, it makes sure we haven't found the bandcamp or an artist with a similar name to a  mainstream artist without a bandcamp. an example I've found is 'beck burger' for 'beck'
                        # also for safe measure is the '[^\w]' part of the regex in case it were 'beckburger': no compound words containing the name we're looking for
                        byline = soup.findAll('span', attrs={'itemprop': 'byArtist'})[0]
                        for a in byline('a'):
                            a.replaceWith(a.renderContents())
                        byline = bl = str(byline.renderContents()).replace('\n', '').strip()
                        r = re.search(self.regexifyBandname(bandname), bl, re.I)
                        bl = bl[bl.find(r.group(0)):].split()
                        if r and len(bandname.split()) == len(bl) and abs(len(byline) - len(bandname) <= 4): # checks for other words or compound words and follows that 4 character rule we use for Wikipedia
                            sources['Bandcamp'] = URL
                            soupREPO['Bandcamp'] = soup                        
                            break
                except:
                    pass
            except:
                pass

        URL = None

        soundcloud_results = self.Google('%s soundcloud' % query, ignoreSuggest)
        for li in soundcloud_results('li'):
            try:
                link = li.div.h3.a
                if re.search('soundcloud.com', link['href']):
                    m = re.search('http://w?w?w?.?soundcloud.com/[^/]*', link['href'])
                    if m:
                        URL = str(m.group(0))
                    soup = BeautifulSoup(br.open(URL).read())
                    header = soup.find('a', attrs={ 'class' : 'user-name' })
                    search, update = self.flexibleComparison(bandname, header.renderContents())
                    if search:
                        sources['Soundcloud'] = URL
                        soupREPO['Soundcloud'] = soup
                        if update != bandname:
                            bandname = update
                        break
            except:
                pass


        # omg find FB!!!! Zuckerbergggg

        facebook_results = self.Google('site:facebook.com %s' % query, ignoreSuggest)
        for li in facebook_results('li'):
            try:
                link = li.div.h3.a
                if re.search('facebook.com', link['href']):
                    URL = link['href'] + '?sk=info'
                    soup = br.open(URL).read()
                    search, update = self.flexibleComparison(bandname, soup)
                    if search and soup.find('Genres') > -1:
                        sources['Facebook'] = URL
                        soupREPO['Facebook'] = soup
                        if update != bandname:
                            bandname = update
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
                knownSources = {'Last.fm': 'last.fm/music', 'ReverbNation': 'reverbnation.com'}
                for entry in knownSources:
                    try:
                        temp = link['href'].index(knownSources[entry])
                        #so it doesn't redefine entries with lower results:
                        if entry in sources:
                            break
                        try:
                            #print '.', knownSources[entry], self.sanitize(bandname) 
                            #print link['href']
                            URL = FBURL = link['href']
                            if entry == 'Last.fm': # make sure to go to the artist's root page and not videos or something
                                m = re.match('http://www.last.fm/music/[^/]*', sources[entry])
                                if m:
                                    URL = m.group(0)
                            source = br.open(URL).read()
                            soup = BeautifulSoup(source)
                            search, update = self.flexibleComparison(bandname, soup)                                        
                            if search:
                                URL = re.match('[^?]*', str(link['href'])).group(0)
                                sources[entry] = URL
                                if entry == 'Facebook': 
                                    soup = source # Facebook compiles in a non-BeautifulSoup-friendly way :( so we deal with it as a string
                                    sources[entry] = FBURL

                                soupREPO[entry] = soup
                                if update != bandname:
                                    bandname = update

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

                for td in genreInfo('td'):
                    td.replaceWith(td.renderContents())
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
            
            try:
                if not nameFormatted:
                    temp = soup.find('div', attrs={ 'id' : 'user-info'})                    
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
                
                print genres
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
            try:
                genres = parts[3].strip().replace('\r', '').split(' / ')
                reverbnationINFO['Genres'] = self.cleanGenres(genres, bandname)
                GENRES += reverbnationINFO['Genres']            
            except: # maybe they just have a location or something
                pass
            # reverb puts a limit of 2 on genres and some people list one as a list of more fuck all

        

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
            if not nameFormatted:
                pr = soup.find('<title>')
                if pr > -1:
                    header = soup[pr + 7:]
                    header = header[:header.find(' | Facebook')]
                    bandname = header.replace(' - Info', '')
                    nameFormatted = True
                

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
        

        # quality control
        
        INFO[0] = INFO[0].strip()
        
        INFO[2] = INFO[2].strip()
        
        
        #Don't bother saying 'US'
        
        
        # return if we have something

        if len(INFO[1]) != 0:
            INFO[0] = INFO[0].decode('utf-8')
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

        splitThese = []

        for i,g in enumerate(genres): # sometimes genres will be seperated by commas or slashes and it wont be caught by the default algorithm so just double-check and split any that may be clumped together swag 
            genres[i] = g = g.strip()
            for d in [',', '/']:
                if len(g.split(d)) > 1:
                    if g[0] == d:
                        genres[i] = g = g[1:]
                    if g[-1] == d:
                        genres[i] = g = g[:-1] # dont start or end with dat shit #UselessSourceCodeComments
                    splitThese.append(g)
                    fixed = g.split(d)
                    toRemove = []
                    for i, n in enumerate(fixed):
                        if n == '':
                            toRemove.append(n)
                    for n in toRemove:
                        fixed.remove(n)
                    genres += fixed
                    break
        for r in splitThese:
            genres.remove(r)


        # capitalize
        for ind,genre in enumerate(genres):
            if genre not in rewords.itervalues():
                ind = genres.index(genre)
                genres[ind] = string.capitalize(genre.strip().replace('&#160;', ' '))


        

        return genres


    
    def chooseGenres(self, genres):
        workingList = []
        overlaps = []
        done = False

        lastResorts = ['Electronic', 'Electronica', 'Indie', 'Rock', 'Alternative', 'Spoken word'] # prefer to remove genres that don't really mean shit but they can be a last resort. this usually leads scapebot to pick more interesting genres :)




    

        remove = []
        for i, n in enumerate(genres):      
            for resort in lastResorts:
                if re.match(resort, n, re.I):
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

        print 'rest', rest, 'overlaps', overlaps
        
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
        majorCities = { 'Seattle|Seatle|Seatttle': 'Seattle', 'Boston': 'Boston', 'Los Angeles': 'LA', 'Portland': 'Portland', 'Long Beach, California': 'Long Beach', 'San Fransisco': 
                        'SF', 'Minneapolis': 'Minneapolis', 'Vancouver, BC': 'Vancouver, BC',
                        'New York City|New York, New York': 'NYC'}

        # neighborhoods and places known by name alone. so far just CA and NYC ,'>/
        #            NYC:                                                                                      CA:
        thatsIt = [ 'Brooklyn', 'Yonkers', 'Manhattan', 'The Bronx', 'Queens', 'Staten Island', 'Long Island', 'Berkeley', 'Long Beach', 'Echo Park', 'Orange County', 'Compton', 'Watts',
                    'Providemce' ] 

        # No postal codes!
        states = { 'Mississippi': 'MS', 'Oklahoma': 'OK', 'Wyoming': 'WY', 'Minnesota': 'MN', 'Alaska': 'AK', 'Illinois': 'IL', 'Arkansas': 'AR', 'New Mexico': 'NM', 'Indiana': 'IN', 'Maryland': 'MD', 
                    'Louisiana': 'LA', 'Texas': 'TX', 'Iowa': 'IA', 'Wisconsin': 'WI', 'Arizona': 'AZ', 'Michigan': 'MI', 'Kansas': 'KS', 'Utah': 'UT', 'Virginia': 'VA', 'Oregon': 'OR', 'Connecticut': 'CT', 
                    'Tennessee': 'TN', 'New Hampshire': 'NH', 'Idaho': 'ID', 'West Virginia': 'WV', 'South Carolina': 'SC', 'California': 'CA', 'Massachusetts': 'MA', 'Vermont': 'VT', 'Georgia': 'GA', 
                    'North Dakota': 'ND', 'Pennsylvania': 'PA', 'Florida': 'FL', 'Hawaii': 'HI', 'Kentucky': 'KY', 'Rhode Island': 'RI', 'Nebraska': 'NE', 'Missouri': 'MO', 'Ohio': 'OH', 'Alabama': 'AL', 
                    'South Dakota': 'SD', 'Colorado': 'CO', 'New Jersey': 'NJ', 'Washington': 'WA', 'North Carolina': 'NC', 'New York': 'NY', 'Montana': 'MT', 'Nevada': 'NV', 'Delaware': 'DE', 'Maine': 'ME' }

        stateInd = -1

        # Don't both specifying states of major cities
        for name in thatsIt:
            if re.search(name, origin, re.I):
                origin = name
                nickname = True
                break
        if not nickname:
            for city in majorCities:
                if re.search(city, origin, re.I):
                    origin = majorCities[city]
                    nickname = True
                    break
            

                
    

     

        # Change postal abbreviation to full state name 
        if not nickname:


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






    def freeBrowser(self):
        br = Browser()
        br.set_handle_robots(False)
        br.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.202 Safari/535.1')]
        return br






    # Scraping functions begin here!


    # All venues have functions for A) Specific date and B) Upcoming future if their homepage is formatted that way (EX: Neumos's). The latter is for efficiency and to leave as small a footprint as possible 
    # Format: [ showID, venueID, Date, Time, Price, 21+, Bands ]



    #pre: pass in a date in ddmmyy fashion :)
    #post: returns a list of information on the show

    def rid(self, phrase):
        for word in ['and', 'with', '&']:
            while phrase.find(word) != -1:
                phrase = phrase.replace(word, ' , ')
        if ':' in phrase:
            phrase = phrase.split(':')
            return phrase[1]
        return phrase    

    def scrapeBlog_TIG(self, band):
        band = band.lower()
        br = self.freeBrowser()
        br.open('http://www.threeimaginarygirls.com/')
        br.select_form(nr=0)
        br.form['q'] = band
        searchPage = br.submit().read()
        soup = BeautifulSoup(searchPage)
        link = soup.findAll(attrs={'class': 'gs-title'})
        print link
        print br.title()
        soup = BeautifulSoup(br.follow_link(nr = 0))
        soup.prettify()
        print soup

   
    def scrapeVenue_crocodile(self, date):
        result = []
        bands = []
        dayInt = 0
        day = date[2:4]
        month = date[0:2]
        if date[4:6]:
            year = '20' + date[4:6]
        br = self.freeBrowser()
        soup = BeautifulSoup(br.open('http://thecrocodile.com/index.html?page=calendar&month=' + thisYear + month).read())
        calendar = soup.find('div', attrs={'id' : 'fullCalendar'})
        counter = 0
        for li in calendar('li'):
            try: 
                li['class']
            except:
                counter += 1
            if counter == int(day) and li.a:
                result.append(month + day + year)
                soup = BeautifulSoup(br.follow_link(url = li.a['href']).read())
                heading = str(soup.find('h3'))
                heading = heading.replace('<h3>', '').replace('</h3>', '')
                heading = self.rid(heading)
                bands = re.findall(r'[\w\s]+', heading )
                
                for i,n in enumerate(bands):
                        bands[i] = n.strip()
                notes = soup.find('p')
                notes = str(notes)
                notes = notes.replace('\n', '')
                notes = notes.replace(' ', '')
                notes = notes.split('<br/>')
                
                time = notes[0]
                time = time.replace('<p>', '')
                time = time.replace('doors', '')
                result.append(time)
                is21 = notes[0]
                if '21' in is21:
                    result.append(True)
                else:
                    result.append(False)
                result.append(bands)
                break
            else:
                pass
        return result
            

    #pre: pass in the date in mmddyy fashion and just the first name of the venue. i.e. moore and not moore theater. Both Streeengs plz &^)
    #post: returns a list of show details    
    def scrapeVenue_STG(self, br, date = None, venue = None, action='scrape', soup = None, month = None):
        if action == 'open':
            URL = 'http://stgpresents.org/calendar/calendar.asp?venue=' + { 'moore': 'moore', 'neptune': 'neptune', 'paramount': 'pmt' }[venue]
            return BeautifulSoup(br.open(URL + '&month=' + month + '&year=' + thisYear).read())
        else:
            month = date[0:2]
            if month[0] == '0':
                month = month[1]
            day = date[2:4]
            if day[0] == '0':
                day = day[1]
            result = []
            bands = []
            test = ''
            hasBreak = '<br'
            shows = soup.findAll('td', attrs={'class': 'calendar-day'})
            for show in shows:
                if show.p.renderContents() == day:
                    result.append(date)
                    findTime = show.findAll('span', attrs={'class': 'venue' + venue.capitalize()})
                    if len(findTime) > 1:
                        time = findTime[len(findTime) - 1]
                    elif len(findTime) == 0:
                        return []
                    else:
                        time = findTime[0]
                    result.append(time.renderContents())
                    findShow = show.findAll('a', attrs={'class': 'venue' + venue.capitalize()})
                    if len(findShow) > 1:
                        goToShow = findShow[len(findShow) - 1]
                    else:
                        goToShow = findShow[0]
                    if goToShow.renderContents().find('Free Neptune') == -1:
                    
                        bands.append(goToShow.renderContents())
                        #go to next page to find 21+ & price
                        linkText = goToShow.renderContents()
                        if linkText.find('&amp;'):
                            linkText = linkText[:linkText.find('&amp;')]
                        soup = BeautifulSoup(br.follow_link(text_regex = linkText).read())
                        
                        #do price
                        price = soup.find(attrs={'class' : 'aPrice'})
                        parsedPrice = [ ] 
                        if price:
                            price = price.renderContents()
                            dict = None
                            priceItems = re.findall(r'\$[/\$\w\s]+', price)
                            for i,x in enumerate(priceItems):
                                
                                y = re.findall('\$\w+', x)
                                if len(y) > 1: # if two prices in one line nigguh
                                    for ind,n in enumerate(y):
                                        dict = [ ]
                                        for p in ['advance', 'day of', 'uw student']:
                                            if re.search(p, x, re.I):
                                                dict.append(p)
                                    print dict
                                    if dict and 'uw student' in dict:
                                        for t, r in enumerate(dict):
                                            if r.find('student') == -1:
                                                UWindex = t
                                    parsedPrice.append( (y[0] + '(' + y[1] + 'UW)' + {'advance': 'ADV', 'day of': 'DAYOF'}[dict[UWindex]] if len(dict) > 1 else None) )                                                                              
                                elif len(y) == 1:
                                    price = y[0]
                                    if re.search('advance', x, re.I):
                                        parsedPrice.append(price + 'ADV')
                                    if re.search('uw student', x, re.I):
                                        parsedPrice.append(price + 'UW')
                                    if re.search('day of show', x, re.I):
                                        parsedPrice.append(price + 'DAYOF')
                            result.append(''.join(parsedPrice) if parsedPrice else price)
                        else:
                            result.append("Free")
                            pass
                        #do 21+
                        age = soup.find(attrs={'class' : 'aNotes'})
                        if age != None:
                            age = age.renderContents()
                            if  '21' in age:
                                result.append(True)
                            else:
                                result.append(False)
                        else:
                            result.append(False)
                            pass
                        #add other bands :^)   need to solve for other cases!!!
                        guests = soup.find(attrs={'id' : 'aGuest'})
                        br.back()
                        
                        if guests != None:
                            guests = guests.renderContents()
                            guests = guests.split('<br />')
                            guests = guests[1].replace('"', '').split(',')
                            bands += guests
                            for i,n in enumerate(bands):
                                bands[i] = n.strip()
                            result.append(bands)
                        else:
                            result.append(bands)
                            pass
                    else:
                        result = []
                else:
                    pass
            return result
    
     
    def Comet_Tavern(self, date):
        br = self.freeBrowser()
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
        br = self.freeBrowser()
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

    def scrapeVenue_neumos(self, date):
        br = self.freeBrowser()
        bandList = []
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
                    bandList.append(band)
                show.append(bandList)
                return show
        except:
                return 'No show that day.'



    def scrapeVenue_jazzAlley(self, date):
        result = []
        band = []
        result.append(date)
        br = self.freeBrowser()
        soup = BeautifulSoup(br.open('http://www.jazzalley.com/calendar.asp').read())
        weeks = soup.findAll('table', attrs={'height': '60', 'border': '0', 'cellspacing': '4', 'cellpadding': '2'})
        for week in weeks:
            days = week.findAll('td', attrs={'bgcolor': '#9f7800'})
            showinfo = week.findAll('td')[8]
            for entry in days:
                day = entry.find('font', attrs={'size': '2'}).renderContents().replace('<b>','').replace('<br />', '').replace('</b>', '').strip()
                month = entry.findAll('font', attrs={'size':'1'})[2].renderContents().replace('</b>', '').strip()
                month = str(['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'].index(month) + 1)
                if len(month) == 1:
                    month = '0' + month
                if len(day) == 1:
                    day = '0' + day
                if month + day == date[0:4]:
                    URL = showinfo.a['href']
                    break
        soup = BeautifulSoup(br.open(URL).read())
        header = soup.findAll('span', attrs={'class': 'columnHeader'})[1].renderContents()
        print header



    def Stranger_Music_Listings(self):    # For cross-referencing, supplementing information
        br = self.freeBrowser()
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
        br = self.freeBrowser()
        password = open('twitterpassword.txt').readline()[0:9]
        br.open('https://mobile.twitter.com/session/new')
        br.select_form(nr=0)
        br.form['username'] = 'scapebot'
        br.form['password'] = password
        soup = BeautifulSoup(br.submit().read())
        
        #logged in

        if action[0] == 'tweet':
            br.select_form(nr=0)            
            br['tweet[text]'] = action[1]
            br.submit()

        if action[0] == "search":
            isSearchForm = lambda l: l.action == 'https://mobile.twitter.com/searches'
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
        
        if action[0] == 'trending':
            trending = soup.find('div', attrs={'class': 'search-trends'}).findAll('a')
            links = [ ]
            for a in trending:
                links.append(a)
            chosen = choice(links)
            soup = BeautifulSoup(br.follow_link(url=chosen['href']).read())
            tweets = soup.findAll('div', attrs={'class' : 'list-tweet'} )
            returnTweets = [ ]
            for tweet in tweets:
                sender = tweet.find('strong').a.renderContents()
                message = tweet.find('span', attrs={ 'class' : 'status' } ).renderContents()
                message_soup = BeautifulSoup(message)
                for tag in message_soup.findAll(True):
                    if tag.name == 'a':
                        hashtag = '%s' % tag.renderContents()
                        tag.replaceWith(hashtag)
                message = message_soup.renderContents()
                tweetContents = message
                returnTweets.append(tweetContents)


            
            soup = BeautifulSoup(' '.join(re.findall('\w+', ' '.join(returnTweets))))
            for tag in soup(True):
                tag.replaceWith(tag.renderContents())
            words = [ ]
            for i in range(0, 10):
                word = choice(soup.renderContents().split(' ')).strip()
                if word != 'RT' and word.find('@') == -1 and len(word) > 3 and word.find(chosen.renderContents().replace('#','')) == -1 and word != ' ': 
                    words.append(word.replace(',', ''))
            words += ['420', 'weed', 'bieber']
            chosenToSearch = choice(words)

            soup = BeautifulSoup(' '.join(re.findall('\w+', ' '.join(self.twitter(['search', chosenToSearch])))))
            for tag in soup(True):
                tag.replaceWith(tag.renderContents())
            words = [ ]
            for i in range(0, choice([3, 4])):
                word = choice(soup.renderContents().split(' ')).strip()
                if word != 'RT' and word.find('@') == -1 and len(word) > 3 and word.find(chosen.renderContents().replace('#','')) == -1 and word != ' ': 
                    words.append(word.replace(',', ''))


            final = '#'
            for i, n in enumerate(words): 
                final += string.capitalize(n)
            return final



    def randomWordFromTrending(self):
        pass


    def tweet(self, tweet):
        self.twitter(['tweet', tweet])


    def removeNewlines(self, x):
        for i,n in enumerate(x):
            x[i] = n.replace('\n', '')
        return x


    def generateTweet(self):
        tweet = ''
        greetingsFile = open('greetings.txt', 'rb')
        greetings = self.removeNewlines(greetingsFile.readlines())
        commentaryFile = open('commentary.txt', 'rb')
        commentary = self.removeNewlines(commentaryFile.readlines())
        print choice(greetings)
        print choice(commentary)
        
        return tweet


    def randomSentence(self, band='Wilco'):
        words = ['is', 'are', 'were', 'was']
        word = choice(words)
        br = self.freeBrowser()
        soup = br.open('http://en.wikipedia.org/wiki/Special:Random').read()
        sentences = re.findall(r'[\w\s]+\s%s\s.*' % word, soup)[:-1]
        if sentences: 
            sentence = choice(sentences)
            if sentence[sentence.find(' %s ' % word):sentence.find('.')].find('mandatory') == -1:
                sentence = band + sentence[sentence.find(' %s ' % word):sentence.find('.')]
                sentence = ' '.join(sentence.split()[0:len(sentence.split())-int(random()*2)])
                if sentence.find('<') > -1:
                    sentence = sentence[:sentence.find('<')]
                if len(sentence) > 12:
                    return sentence
                else:
                    self.randomSentence(band)
            else:
                self.randomSentence(band)
        else:
            self.randomSentence(band)


