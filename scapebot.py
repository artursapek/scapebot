''' 
  scapebot is a web spider that can research bands and scrape show information from Seattle venues
  he is basically our slave
  authored by Artur Sapek
  MIT license 
'''

from BeautifulSoup import BeautifulSoup
from mechanize import Browser
from collections import defaultdict
from random import *
try:
    from django.utils import simplejson
except:
    import simplejson
import string
import re
import os
import urllib2


class base():
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
        global locales
        locales = [ 'Aberdeen', 'Adams', 'Airway Heights', 'Algona', 'Anacortes', 'Arlington', 'Asotin', 'Auburn', 'Bainbridge Island', 'Battle Ground', 'Bellevue', 'Bellingham', 'Benton', 'Benton City', 'Bingen', 
                    'Black Diamond', 'Blaine', 'Bonney Lake', 'Bothell', 'Bremerton', 'Brewster', 'Bridgeport', 'Brier', 'Buckley', 'Burien', 'Burlington', 'Camas', 'Carnation', 'Cashmere', 'Castle Rock', 'Centralia', 
                    'Chehalis', 'Chelan', 'Cheney', 'Chewelah', 'Clallam', 'Clark', 'Clarkston', 'Cle Elum', 'Clyde Hill', 'Colfax', 'College Place', 'Columbia', 'Colville', 'Connell', 'Cosmopolis', 'Covington', 'Cowlitz', 
                    'Davenport', 'Dayton', 'Deer Park', 'Des Moines', 'Douglas', 'DuPont', 'Duvall', 'East Wenatchee', 'Edgewood', 'Edmonds', 'Electric City', 'Ellensburg', 'Elma', 'Entiat', 'Enumclaw', 'Ephrata', 'Everett', 
                    'Everson', 'Federal Way', 'Ferndale', 'Ferry', 'Fife', 'Fircrest', 'Forks', 'Franklin', 'Garfield', 'George', 'Gig Harbor', 'Gold Bar', 'Goldendale', 'Grand Coulee', 'Grandview', 'Granger', 'Granite Falls', 
                    'Grant', 'Grays Harbor', 'Harrington', 'Hoquiam', 'Ilwaco', 'Island', 'Issaquah', 'Jefferson', 'Kahlotus', 'Kalama', 'Kamilche', 'Kelso', 'Kenmore', 'Kennewick', 'Kent', 'Kettle Falls', 'King', 'Kirkland', 
                    'Kitsap', 'Kittitas', 'Klickitat', 'La Center', 'Lacey', 'Lake Forest Park', 'Lake Stevens', 'Lakewood', 'Langley', 'Leavenworth', 'Lewis', 'Liberty Lake', 'Lincoln', 'Long Beach', 'Longview', 'Lynden', 
                    'Lynnwood', 'Mabton', 'Maple Valley', 'Marysville', 'Mason', 'McCleary', 'Medical Lake', 'Medina', 'Mercer Island', 'Mesa', 'Mill Creek', 'Milton', 'Monroe', 'Montesano', 'Morton', 'Moses Lake', 'Mossyrock',
                    'Mount Vernon', 'Mountlake Terrace', 'Moxee', 'Mukilteo', 'Napavine', 'Newcastle', 'Newport', 'Nooksack', 'Normandy Park', 'North Bend', 'North Bonneville', 'Oak Harbor', 'Oakville', 'Ocean Shores', 
                    'Okanogan', 'Olympia', 'Omak', 'Oroville', 'Orting', 'Othello', 'Pacific', 'Palouse', 'Pasco', 'Pateros', 'Pend Oreille', 'Pierce', 'Pomeroy', 'Port Angeles', 'Port Orchard', 'Port Townsend', 'Poulsbo', 
                    'Prosser', 'Pullman', 'Puyallup', 'Quincy', 'Rainier', 'Raymond', 'Redmond', 'Renton', 'Republic', 'Richland', 'Ridgefield', 'Ritzville', 'Rock Island', 'Roslyn', 'Roy', 'Royal City', 'Sammamish', 'SeaTac', 
                    'Seattle', 'Sedro-Woolley', 'Selah', 'Sequim', 'Shelton', 'Shoreline', 'Skagit', 'Skamania', 'Snohomish', 'Snoqualmie', 'Soap Lake', 'South Bend', 'Spokane', 'Spokane Valley', 'Sprague', 'Stanwood', 'Stevens', 
                    'Stevenson', 'Sultan', 'Sumas', 'Sumner', 'Sunnyside', 'Tacoma', 'Tekoa', 'Tenino', 'Thurston', 'Toledo', 'Tonasket', 'Toppenish', 'Tukwila', 'Tumwater', 'Union Gap', 'University Place', 'Vader', 'Vancouver', 
                    'Waitsburg', 'Walla Walla', 'Wapato', 'Warden', 'Washougal', 'Wenatchee', 'West Richland', 'Westport', 'Whatcom', 'White Salmon', 'Whitman', 'Winlock', 'Woodinville', 'Woodland', 'Woodway', 'Yakima', 'Yelm',
                    'Zillah' ]

    def GoogleAPI(self, query, cse):
        queryURL = query.replace(' ', '%20').lower()
        url = 'https://www.googleapis.com/customsearch/v1?key=AIzaSyDP4MJGp7FRuMnKuF3fJ4PbcmpW7w5rOIc&cx=%s&q=%s' % (cse, queryURL)
        request = urllib2.Request(url, None, { 'Referer': 'bandscape.net' })
        response = urllib2.urlopen(request)
        results = simplejson.load(response)['items']
        urls = [ ]
        for r in results:
            urls.append(r['link'].replace('www.', ''))
        urls.sort()
        return urls    

    def massRemove(x, r):
        for w in r:
            x = x.replace(w, '')
        return x
   
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

    
    # pre: a band name
    # post: if not listIt: a regex string for bandname.

    def regexify(self, bandname, listIt=False):
        # regexes for flexibility when checking a page for actual mentions of the name ^_^
        bandname = bandname.lower().replace(' and ', '(\sand\s|\s&\s|\s&amp;\s)').replace(' & ', '(\sand\s|\s&\s|\s&amp;\s)')
        questionOut = ['[', ']']
        change = { 'the ': '(the\s)?', 'DJ ':'(DJ\s)?','dj ':'(dj\s)?',' ':'([-\s,\.]?)+' }
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
        else: # if listIt, do the same shit in a different way that allows it to be returned as a list 
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



class band(base):
                   
    # moves a pair of question marks across the name, character by character. gives some tolerance for typos. fucking dank functions.

    def flexibleComparison(self, bandname, soup=None):
        if len(bandname) > 100:
            tolerance = 2
        else:
            tolerance = 1
        # super dank. the objective: to get a typo like "andrew james robinson" to match with "andrew james robison". a pair of question marks will be gliding across the name.
        found = False
        update = bandname
        if re.search(self.regexify(bandname), str(soup), re.I):
            found = True
        if found == False:
            l = len(bandname)
            for i in range(0, l - 3):
                name = self.regexify(bandname, listIt = True) # list it bitch
                for x in range(i, i + tolerance):
                    try:
                        if name[x][-1] != '?' or name[x][-2] != '?':
                            if name[x] != '([-\s,\.]?)+':
                                name[x] = name[x] + '?\w?' # add a question mark
                    except:
                        pass
                tolerant = ''.join(name)
                try:
                    r = re.search(tolerant, str(soup), re.I)
                    if r:
                        found = True
                        update = r.group(0)                    
                        break
                except:
                    pass
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

    def getSourceURLS(self, bandname, forceLocal):
        x = None
        try:
            x = self.GoogleAPI('"' + bandname + (' seattle' if forceLocal else '') + '"', '014750848680997063315:ienipxcmxo8')
        except:
            self.getSourceURLS(bandname, forceLocal)
        if x == None:
            self.getSourceURLS(bandname, forceLocal)
        else:            
            return x

    # pre: band name, force(Seattle)Local[opt.]
    # post: [ band name, [ genre, genre ], origin, albumcover_src ]
    # * never input ignoreSuggest yourself, this is for recursion
    
    def research(self, bandname, save = False, forceLocal = False, ignoreSuggest = False):
        nameFormatted = False
        sources = {}
        GENRES = TRUSTWORTHY_GENRES = []
        ALBUMCOVER = alternate = results = None
        originalInput = bandname
        soupREPO = wikiINFO = lastfmINFO = soundcloudINFO = bandcampINFO = facebookINFO = myspaceINFO = reverbnationINFO = {}
        
        # Break a few eggs
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


        # Do a Google custom search for bandcamp, wikipedia, myspace, reverbnation, lastfm, facebook, and soundcloud pages the band might own.
        sourceURLS = self.getSourceURLS(bandname, forceLocal)


        # Investigate each source URL, commit it to sources if it passes the check. While we're at it, we also update the band name if it was misspelled.
        # If validation passes, commit it to memory.

        # MYSPACE
        myspaceINFO = { }
        for URL in filter(lambda k: 'myspace.com' in k, sourceURLS):
            try:
                soup = BeautifulSoup(br.open(URL).read())
                header = soup.findAll('h1')[1]
                search, update = self.flexibleComparison(bandname, header.renderContents())
                if search and len(soup.findAll('h3', text='General Info', attrs={ 'class' : 'moduleHead' })) > 0 and soup.find(attrs={'class':'odd BandGenres'}):
                    sources['Myspace'] = URL
                    soupREPO['Myspace'] = soup
                    if update != bandname and not re.search(originalInput, str(soup), re.I):
                        bandname = update
                    break
            except:
                pass

        # WIKIPEDIA
        wikiINFO = { }
        for URL in filter(lambda k: 'wikipedia.org' in k, sourceURLS):
            try:
                soup = BeautifulSoup(br.open(URL).read())
                header = soup.h1.renderContents()
                search, update = self.flexibleComparison(bandname, header)                
                if header.find('song)') == -1 and search and len(soup.findAll('a', href='/wiki/Music_genre')) > 0 and re.search(self.regexify(bandname), header, re.I) and '(soundtrack)' not in header and 'album)' not in header:
                    sources['Wikipedia'] = str(URL)
                    soupREPO['Wikipedia'] = soup
                    if update != bandname and not re.search(originalInput, str(soup), re.I):
                        bandname = update
                    break
            except:
                pass

        # BANDCAMP
        bandcampINFO = { }
        for URL in filter(lambda k: 'bandcamp.com' in k, sourceURLS):
            URL = re.search('.*\.com', URL).group(0) + '/releases'
            try:
                soup = BeautifulSoup(br.open(URL).read())
                byline = soup.findAll('span', attrs={'itemprop': 'byArtist'})[0]
                for a in byline('a'):
                    a.replaceWith(a.renderContents())
                byline = bl = str(byline.renderContents()).replace('\n', '').strip()
                r = re.search(self.regexify(bandname), bl, re.I)
                bl = bl[bl.find(r.group(0)):].split()
                if r and len(bandname.split()) == len(bl) and abs(len(byline) - len(bandname) <= 4):
                    sources['Bandcamp'] = URL
                    soupREPO['Bandcamp'] = soup                        
                    break
            except:
                pass

        # SOUNDCLOUD
        soundcloudINFO = { }
        for URL in filter(lambda k: 'soundcloud.com' in k, sourceURLS):
            try:
                URL = re.search('.*.com/[^/]*', URL).group(0)
                soup = BeautifulSoup(br.open(URL).read())
                header = soup.find('a', attrs={ 'class' : 'user-name' })
                search, update = self.flexibleComparison(bandname, header.renderContents())
                if search and URL.find('search?') == -1:
                    sources['Soundcloud'] = URL
                    soupREPO['Soundcloud'] = soup
                    if update != bandname and not re.search(originalInput, str(soup), re.I):
                        bandname = update
                    break
            except:
                pass

        # FACEBOOK
        facebookINFO = { }
        for URL in filter(lambda k: 'facebook.com' in k, sourceURLS):
            try:
                URL += '?sk=info'
                soup = br.open(URL).read()
                search, update = self.flexibleComparison(bandname, soup)
                if search and soup.find('Genres') > -1:
                    sources['Facebook'] = URL
                    soupREPO['Facebook'] = soup
                    if update != bandname and not re.search(originalInput, str(soup), re.I):
                        bandname = update
                    break
            except:
                pass


        # LAST.FM
        lastfmINFO = { }
        for URL in filter(lambda k: 'last.fm/music/' in k, sourceURLS):
            try:
                source = br.open(URL).read()
                soup = BeautifulSoup(source)
                search, update = self.flexibleComparison(bandname, soup)
                if search:
                    sources['Last.fm'] = re.match('[^?]*', str(URL)).group(0)
                    soupREPO['Last.fm'] = soup
                    if update != bandname:
                        bandname = update
                break
            except:
                pass


        # REVERBNATION
        reverbnationINFO = { }
        for URL in filter(lambda k: 'reverbnation.com' in k and '/show/' not in k, sourceURLS):
            try:
                source = br.open(URL).read()
                soup = BeautifulSoup(source)
                search, update = self.flexibleComparison(bandname, soup)
                if search:
                    sources['ReverbNation'] = re.match('[^?]*', str(URL)).group(0)
                    soupREPO['ReverbNation'] = soup
                    if update != bandname:
                        bandname = update
                break
            except:
                pass
        
        if 'Wikipedia' in sources:
            soup = soupREPO['Wikipedia']
            try:
                possibleName = self.massRemove(soup.h1.renderContents(), [' (musician)', ' (band)', ' (rock band)', 'User:', ' (singer)'])
                if possibleName.find('<i>') < -1:
                    bandname = possibleName
                    nameFormatted = True
                originInfo = soup.findAll('th', text='Origin')[0].parent.parent.td
                for tag in originInfo(True):
                    tag.replaceWith(tag.renderContents())
                origin = originInfo.renderContents()
                wikiINFO['Origin'] = origin
            except:
                pass
            try:
                genreInfo = soup.findAll('th', text='Genres')[0].parent.parent.parent.td
                for tag in genreInfo(True):
                    tag.replaceWith(tag.renderContents())
                genres = genreInfo.renderContents().split(', ')
                if genres[0].find('\n') > -1 and len(genres) == 1:
                    genres = re.sub('\n', ', ', genres[0]).split(', ')
                genres = self.cleanGenres(genres, bandname)
                wikiINFO['Genre'] = genres  
                GENRES += genres
            except:
                pass

        if 'Last.fm' in sources:
            try:
                lastfmINFO = {}
                soup = soupREPO['Last.fm']
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
                        nameFormatted = True
                    genres = self.cleanGenres(genres, bandname)
                    GENRES += genres                    
                    TRUSTWORTHY_GENRES += genres
                except:
                    pass
                
                try:
                    soup = str(soup)
                    localityInd = soup.index('p class="origin"')
                    locality = soup[localityInd:]
                    locality = locality[locality.find('<strong>') + 8:]
                    locality = locality[:locality.index('\n')]
                    locality = BeautifulSoup(locality)
                    for span in locality('span'):
                        span.replaceWith(span.renderContents())
                    locality = str(locality)
                except:
                    pass
                lastfmINFO['Genre'] = genres
                if locality != '</strong>':
                    lastfmINFO['Origin'] = locality
            except:
                pass

        if 'Soundcloud' in sources:
            soundcloudINFO = {'Genres': []}
            soup = soupREPO['Soundcloud']

            target = soup.findAll('span', { 'class' : 'genre' })
            for genre in target:
                if genre.renderContents() not in soundcloudINFO['Genres']:
                    soundcloudINFO['Genres'].append(genre.renderContents())
            soundcloudINFO['Genres'] = self.cleanGenres(soundcloudINFO['Genres'], bandname)

            GENRES += soundcloudINFO['Genres']
            temp = soup.find('div', attrs={ 'id' : 'user-info'})                    
            try:
                soundcloudINFO['Origin'] = temp.span.renderContents()
            except:
                pass
            try:
                if not nameFormatted and not re.search(originalInput, str(soup), re.I):
                    bandname = temp.h1.renderContents()[:temp.h1.renderContents().find('\n')]
                    nameFormatted = True
            except:
                pass

        if 'Myspace' in sources:
            myspaceINFO = {}
            soup =  soupREPO['Myspace']
            try:    
                target = soup.findAll(attrs={'class':'odd BandGenres'})[0]
                for tag in target.findAll(True):
                    tag.replaceWith(tag.renderContents())
                target = target.renderContents()[8:]
                genres = self.cleanGenres(target.split(' / '), bandname)
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
            try:
                info = soup.findAll('div', attrs={ 'class' : 'location_genres' })[0].renderContents() # all we need
                parts = info.split('\n')
                reverbnationINFO['Origin'] = parts[1].strip().replace('\r', '')
                try:
                    genres = parts[3].strip().replace('\r', '').split(' / ')
                    reverbnationINFO['Genres'] = self.cleanGenres(genres, bandname)
                    GENRES += reverbnationINFO['Genres']   
                except:
                    pass
            except:
                pass
            if not nameFormatted:
                try:
                    title = re.search(r'<title>.*</title>', str(soup), re.I).group(0).replace('<title>', '')
                    bandname = title[:title.find('|')].strip()
                    nameFormatted = True
                except:
                    pass

        if 'Facebook' in sources: # doesn't use BeautifulSoup because Facebook compiles really fucking weird
            facebookINFO = {}
            soup = soupREPO['Facebook']
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
                    if not nameFormatted:
                        namesection = soup.findAll('dl', attrs={ 'id' : 'name-section' })[0]
                        artistname = namesection.span
                        for a in artistname('a'):
                            a.replaceWith(a.renderContents())
                        bandname = artistname.renderContents().split()
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
            # ALBUM COVER
            ALBUMCOVER = soup.find('a', attrs={'href': '/no_js/show_tralbum_art'}).img['src']
            

        # Site scraping is complete. Not let's parse the data! *:^)-)-<


        if not nameFormatted: # if we never got to format the name from one of their pages, just capitalize it all by default
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

        # final all-encompassing quality control
        INFO[0] = INFO[0].strip()
        if type(INFO[1]) == list:
            for i, g in enumerate(INFO[1]):
                INFO[1][i] = g.strip()
        elif type(INFO[1]) == str:
            INFO[1] = INFO[1].strip()
        INFO[2] = INFO[2].strip()
        if len(INFO[2]) == 2:
            INFO[2] = INFO[2].upper() # state/country initials
        INFO[0] = INFO[0].decode('utf-8')
        if save:
            g = self.get(bandname)
            if not g:
                b = Band(bandname=INFO[0], genre=INFO[1], origin=INFO[2], listen=INFO[3])
                b.save()
                if ALBUMCOVER:
                    self.cover(b.id, src=ALBUMCOVER)
                return b
            else:
                g.bandname = INFO[0]
                g.genre = INFO[1] 
                g.origin = INFO[2]
                g.listen = INFO[3]
                g.save()
                if ALBUMCOVER:
                    self.cover(g.id, src=ALBUMCOVER)
                return g
        return INFO
        # ta-dah!










# ------ helper functions for band.research()

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
                        'Minimalist', 'Australian', '80', '70', 'Music', 'Song', 'Comedy', 'Interview', 'Talk Radio', 'Talk', 'Los angeles'] # "All music is experimental." - Partick Leonard
        bannedGenres += states + locales
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
                    if toRemove.count(genre) == 0:
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
        
        # Prefer to remove genres that don't really mean shit but they can be a last resort. this usually leads scapebot to pick more interesting genres :)
        lastResorts = ['Electronic', 'Electronica', 'Indie', 'Rock', 'Alternative', 'Spoken word'] 

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
        
        rest = list(set(genres).difference(set(overlaps)))
        
        for genre in overlaps:
            if overlaps.count(genre) > 1:
                overlaps.remove(genre)

        
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
