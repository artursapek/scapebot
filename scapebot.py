''' scapebot is a web spider that can research bands and scrape show information from Seattle venues
    he is basically our slave
    authors: Artur Sapek, Michael Beswetherick '''

from BeautifulSoup import BeautifulSoup
from mechanize import Browser
from collections import defaultdict
from datetime import datetime
from django.utils import simplejson
from time import sleep
try: from main.models import *
except: pass
try: from PIL import Image as img
except: pass
from random import *
import string
import re
import os
import urllib2
import datetime


class base():
    def __init__(self):
        global NOW
        d = datetime.datetime.now()
        NOW = [d.year, d.month, d.day]
        global months 
        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        global monthsabbr 
        monthsabbr = ['Jan', 'Feb', 'Mar', 'April', 'May', 'June', 'July', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        global months3
        months3 = ['Jan','Feb','Mar','Apr','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
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
       

    def sanitize(self, x):
        for i in range(1, 32):
            x = ''.join(x.split(str(string.punctuation)[i]))
        return x

    def search(self, y, x):
        if type(x) not in [str, unicode]:
            x = x.renderContents()
        r = re.search(y, x, re.I)
        if r: return r.group(0)
        else: return ''

    def cleanText(self, s):
        s = BeautifulSoup(str(s)) # I think this is necessary
        for tag in s(True):
            tag.replaceWith(tag.renderContents())
        return s.renderContents().strip()


    def GoogleAPI(self, query, cse):
        if query == '' or len(query) == 1: # These will fuck it right up and eat API calls
            return [ ]
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

    def parseListing(self, query):
        queries = [ query ]
        for x in [' with ', ' & ', ' and ', ' - ', ': ']:
            find = query.find(x)
            if find > -1:
                queries.append(query[:find].strip())
        return queries
    
    def freeBrowser(self):
        br = Browser()
        br.set_handle_robots(False)
        br.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.202 Safari/535.1')]
        return br

    def regexify(self, query, listIt=False):
        spaceReplace = '[\\[\\]\\(\\)\\s\\.\\,\\-\\.]+?'
        prefixSuffix = '[\\[\\]\\(\\)\\s\\.\\,\\-]?'
        # regexes for flexibility when checking a page for actual mentions of the name ^_^
        query = query.lower().replace(' and ', '(\sand\s|\s&\s|\s&amp;\s)').replace(' & ', '(\sand\s|\s&\s|\s&amp;\s)')
        questionOut = ['[', ']']
        change = { 'the ': '(the\s)?', 'DJ ':'(DJ\s)?','dj ':'(dj\s)?',' ':spaceReplace}
        if not listIt:
            for q in questionOut:
                query = query.replace(q, q + '?')
            for c in change:
                query = query.replace(c, change[c])
            r = u''
            for i in query: # take care of unicode chars. shitty metal bands often use special characters to look hardcore
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
            return '%s%s%s' % (prefixSuffix, r, prefixSuffix)
        else: # if listIt, do the same shit in a different way that allows it to be returned as a list 
            changed = []
            for i,n in enumerate(query):
                for ind,ch in enumerate(change):
                    if query[i:i + len(ch)] == ch:
                        culprit = query[i:i + len(ch)]
                        for duba in range(0, query.count(culprit)):
                            w = query.find(culprit) # im running out of variables
                            if w != -1:
                                query = query[:w] + change[ch] + query[w + 1:]
                                changed.append([w, len(change[ch])]) # commit
                        # now we have an array like this [[1, 3], [5, 6]] for the fuckin indeces in the string to keep together in the list YO! so we can iterate over them as one. fuckall.
            l = []
            skip = 0
            for ind,i in enumerate(query): # take care of unicode chars. shitty metal bands often use special characters to look hardcore
                r = ''
                stop = False
                if skip > 0:
                    skip -= 1
                else:
                    for y,x in enumerate(changed):
                        if ind == changed[y][0]:
                            l.append(query[ind:ind+changed[y][1]])
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
            l.insert(0, prefixSuffix)
            l.append( prefixSuffix )

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
                            if name[x] != '[\\[\\]\\(\\)\\s\\.\\,\\-]+?' and name[x] != '[\\[\\]\\(\\)\\s\\.\\,\\-]?':
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


    
    def getSourceURLS(self, bandname, forceLocal):
        print bandname, '...'
        x = None
        try:
            x = self.GoogleAPI(bandname + (' seattle' if forceLocal else ''), '014750848680997063315:ienipxcmxo8')
        except:
            pass
        if x == None:
            print 'API returned nothing! Waiting 5 seconds...'
            sleep(5) # WAIT A FEW SECONDS BEFORE YOU TRY AGAIN OR THE API GETS EATEN UP AND I LOST LIKE 3 DOLLARS FOR NOTHING
                     # UGH
            print 'Trying again. Query: %s ' % bandname 
            self.getSourceURLS(bandname, forceLocal)
        else:            
            return x

    # pre: band name, force(Seattle)Local[opt.]
    # post: [ band name, [ genre, genre ], origin, albumcover_src ]
    # * never input ignoreSuggest yourself, this is for recursion
    
    def research(self, bandname, save = False, raw = False, forceLocal = False, givenSources = {}):
        if bandname == '' or len(bandname) == 1:
            print 'ERROR: bad or empty name'
            return None
        sources = {}
        for g in givenSources:
            sources[g] = givenSources[g]
        nameFormatted = False
        GENRES = TRUSTWORTHY_GENRES = []
        ALBUMCOVER = results = None
        originalInput = bandname
        soupREPO = wikiINFO = lastfmINFO = soundcloudINFO = bandcampINFO = facebookINFO = myspaceINFO = reverbnationINFO = {}
        
        # Break a few eggs
        br = self.freeBrowser()

        # Do a Google custom search for bandcamp, wikipedia, myspace, reverbnation, lastfm, facebook, and soundcloud pages the band might own.
        sourceURLS = self.getSourceURLS(bandname, forceLocal)


        # Investigate each source URL, commit it to sources if it passes the check. While we're at it, we also update the band name if it was misspelled.
        # If validation passes, commit it to memory.

        # MYSPACE
        myspaceINFO = { }
        urls = filter(lambda k: 'myspace.com' in k, sourceURLS)
        urls.reverse()
        for URL in urls:
            try:
                URL = re.search('.*.com/[^/]*', URL).group(0)
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
        urls = filter(lambda k: 'wikipedia.org' in k and not re.search('album|File:', k), sourceURLS)
        urls.reverse()
        for URL in urls:
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
        urls = filter(lambda k: 'bandcamp.com' in k, sourceURLS) # No regex required for bcamp
        urls.reverse()
        for URL in urls:
            URL = re.search('.*\.com', URL).group(0) + '/releases'
            try:
                soup = BeautifulSoup(br.open(URL).read())
                byline = soup.findAll('span', attrs={'itemprop': 'byArtist'})[0]
                for a in byline('a'):
                    a.replaceWith(a.renderContents())
                byline = bl = byline.renderContents().replace('\n', '').strip()
                r = re.search(self.regexify(bandname), bl, re.I) # 
                bl = bl[bl.find(r.group(0)):].split()
                if r and len(bandname.split()) == len(bl) and abs(len(byline) - len(bandname) <= 4):
                    sources['Bandcamp'] = URL
                    soupREPO['Bandcamp'] = soup
                    break
            except:
                pass

        # SOUNDCLOUD
        soundcloudINFO = { }
        urls = filter(lambda k: 'soundcloud.com' in k, sourceURLS)
        urls.reverse()
        for URL in urls:
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
        urls = filter(lambda k: 'facebook.com' in k, sourceURLS)
        urls.reverse()
        for URL in urls:
            try:
                URL = re.search('.*.com/[^/]*', URL).group(0) + '?sk=info'
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
        urls = filter(lambda k: 'last.fm/music/' in k, sourceURLS)
        urls.reverse()
        for URL in urls:
            try:
                URL = re.search('.*.fm/music/[^/]*', URL).group(0)
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
        urls = filter(lambda k: 'reverbnation.com' in k, sourceURLS)
        urls.reverse()
        for URL in urls:
            try:
                URL = re.search('.*.com/[^/]*', URL).group(0)
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
    
        
        if 'Wikipedia' in soupREPO:
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
                genres = [g.renderContents() for g in soup.findAll('th', text='Genres')[0].parent.parent.parent.td.findAll('a', attrs={'href': re.compile('/wiki/.*')})]
                genres = self.cleanGenres(genres, bandname)
                wikiINFO['Genre'] = genres  
                GENRES += genres
            except:
                pass

        if 'Last.fm' in soupREPO:
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

        if 'Soundcloud' in soupREPO:
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

        if 'Myspace' in soupREPO:
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

        if 'ReverbNation' in soupREPO:
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

        if 'Facebook' in soupREPO: # doesn't use BeautifulSoup because Facebook compiles really fucking weird
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

        if 'Bandcamp' in soupREPO:
            bandcampINFO = {}
            soup = soupREPO['Bandcamp']
            tags = [a.renderContents() for a in soup.findAll('a', attrs={ 'href' :re.compile('.*.com/tag/.*') })]
            x = 1
            if tags:
                possibleOrigin = tags[-1]
                if possibleOrigin[0].isupper():
                    bandcampINFO['Origin'] = possibleOrigin
                    x = 2
                if len(tags) == 2 and len(tags[0].split(' ')) > 3:
                    bandcampINFO['Genres'] = tags[0].split(' ')
                elif len(tags) > 0:
                    bandcampINFO['Genres'] = tags[:len(tags) - x]
                GENRES += self.cleanGenres(bandcampINFO['Genres'], bandname)
            if not nameFormatted:
                namesection = soup.findAll('div', attrs={ 'id' : 'name-section' })[0]
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
            try:
                ALBUMCOVER = soup.find('a', attrs={'href': '/no_js/show_tralbum_art'}).img['src']
            except: pass    


        # Site scraping is complete. Not let's parse the data! *:^)-)-<

#        print sources

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
        if type(INFO[1]) == str:
            INFO[1] = INFO[1].strip()
        INFO[2] = INFO[2].strip()
        if len(INFO[2]) == 2:
            INFO[2] = INFO[2].upper() # state/country initials
        INFO[0] = INFO[0].decode('utf-8')
        if save:
            b = self.get(bandname)
            if not b:
                b = Band(name=INFO[0], genre=INFO[1], origin=INFO[2])
                for s in sources:
                    setattr(b, s.lower().replace('.',''), sources[s]) # Save the sources :)
                b.save()
                return b
            else:
                b.bandname = INFO[0]
                b.genre = INFO[1] 
                b.origin = INFO[2]
                for s in sources:
                    setattr(b, s.lower().replace('.',''), sources[s])
                b.save()
                return b
            if ALBUMCOVER:
                self.cover(src=ALBUMCOVER, band=b)
        if raw:
            b = {'name': INFO[0], 'genre': INFO[1], 'origin': INFO[2], 'sources': [s for s in sources.itervalues()]}
            return b

        return INFO, sources
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
                        'Minimalist', 'Australian', '80', '70', 'Music', 'Song', 'Comedy', 'Interview', 'Talk Radio', 'Talk', 'Los angeles', 'Live'] # "All music is experimental." - Partick Leonard
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
#        print genres

        g = []
        for genre in genres:
            if genre != '':
                g.append(genre)
        genres = g

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
            #   print word, occurrences
        
        rest = list(set(genres).difference(set(overlaps)))
        
        for genre in overlaps:
            if overlaps.count(genre) > 1:
                overlaps.remove(genre)

#        print 'rest', rest, 'overlaps', overlaps
        
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
#        print workingList
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
#        print workingList    
            

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
                        'SF', 'Minneapolis': 'Minneapolis', 'Vancouver, BC': 'Vancouver, BC', 'New York City|New York, New York': 'NYC'}
        # neighborhoods and places known by name alone. so far just CA and NYC ,'>/
        #            NYC:                                                                                      CA:
        thatsIt = [ 'Brooklyn', 'Yonkers', 'Manhattan', 'The Bronx', 'Queens', 'Staten Island', 'Long Island', 'Berkeley', 'Long Beach', 'Echo Park', 'Orange County', 'Compton', 'Watts', 'Providence' ] 
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
            r = re.search(',?\s?united states', origin, re.I)
            if r: origin = origin.replace(r.group(0), '')
            r = re.search(', Please Select Your Region', origin, re.I)
            if r: origin = origin.replace(r.group(0), '')

            
            origin = origin.strip()

            # check for abbreviation
            r = re.match('(?P<a>\w+)[\s,]+(?P<b>\w\w)$', origin)
            if r:
                if r.group('b').lower() != 'us':
                    origin = origin.replace(r.group('b'), r.group('b').upper())
        return origin




    def get(self, choice):
        if not choice:
            return None
        if type(choice) == int:
            band = Band.objects.filter(id=choice)
            if len(band) == 1:
                return band[0]
            else:
                return None
        elif type(choice) == str:
            band = Band.objects.filter(name__iexact=choice)
            if len(band) == 1:
                return band[0]
            else:
                return None

    def touch(self, choice, genre=None, origin=None, cover=None):
        band = self.get(choice)
        try: c = band.cover
        except: c = ''
        try: o = band.origin
        except: o = ''
        try: g = band.genre
        except: g = ''
        if genre == None and origin == None and cover == None:
            return [band.id, band.name, g, o, c]
        else:
            band.genre = genre if genre != None else g
            band.origin = origin if origin != None else o
            band.cover = cover if cover != None else c
            band.save()
            return [band.id, band.name, band.genre, band.origin, band.cover]

    def cover(self, choice=None, src=None, band=None): # swag
        br = self.freeBrowser()
        if not choice and not band:
            return None
        band = self.get(choice) if choice else band       
        if not src:
            breakNow = False
            albumsRepo = { }
            result = [ ]
            albumSRC = ''
            URL = filter(lambda f: '/' + band.name.lower().replace(' ', '-') + '/' in f, self.GoogleAPI(band.name, '014750848680997063315:uwrdxv39alm'))[0]
            print URL
            if URL:
                soup = BeautifulSoup(br.open(URL).read())
                if re.search(self.regexify(band.name), soup.h1.renderContents(), re.I):
                    albums = soup.findAll('img', attrs={'class': 'artwork'})
                    for a in albums:
                        if a['src'].find('/Music/') > -1:
                            albumSoup = BeautifulSoup(br.open(a.parent.parent['href']).read())
                            release = albumSoup.find('li', attrs={'class': 'release-date'})
                            # Ignore non-albums (reprises, singles, reissues)
                            try: 
                                if not re.search('- Single|\(.*Deluxe.*\)|th Anniversary.*\)|Edition.*\)|Best of|Boxed Set|Live at|Bootleg|Concert|Festival|Compilation|\(.*Promo.*\)', albumSoup.h1.renderContents(), re.I): 
                                    year = re.search('20\d\d|19\d\d', release.renderContents()).group(0)
                                    albumBig = albumSoup.findAll('div', attrs={'class': 'artwork'})
                                    for alb in albumBig:
                                        try:
                                            if alb.img['src'].find('170x170-75') > -1:
                                                albumSRC = alb.img['src']
                                        except:
                                            pass
                                    if not year in albumsRepo:
                                        albumsRepo[year] = albumSRC
                            except:
                                pass
            if albumsRepo:
                pairs = albumsRepo.items()
                pairs.sort()
                albumSRC = str(pairs[-1][1])
        else:
            albumSRC = src
        print albumSRC
        if albumSRC:
            dl = br.retrieve(albumSRC)[0]
            cover = img.open(dl)
            cover.thumbnail( ( 170, 170), img.ANTIALIAS)
            cover.save('/home/bandscape/dev/bandscape/main/static/img/covers/%s/%s.jpg' % (band.name.lower().replace('the ', '')[0], ''.join(re.findall('\w', band.name)).lower()), "JPEG", quality=90) 
            cover.thumbnail( ( 60, 60), img.ANTIALIAS)
            cover.save('/home/bandscape/dev/bandscape/main/static/img/covers/%s/%s__.jpg' % (band.name.lower().replace('the ', '')[0], ''.join(re.findall('\w', band.name)).lower()), "JPEG", quality=90) 
            return



# ----


# ----



class venue(base):

    def scrape(self, venue, date): # Usage: venue.scrape(12, '0208') scrapes Neptune Theater for Feb 8
        br = self.freeBrowser()
        S = getattr(self, 'scv_' + ('M_' if len(date) <= 2 else '') + str(venue))(date, br)   # Venue scraping functions are named with their id. scv_1 is Neumos, so scv_1('0214') gets the show (or None) for Neumos on Valentines day 
        return [ {'venue': s[0], 'date': s[1], 'time': s[2], 'price': s[3],                   # An extra _M denotes is an efficient function for the entire month, so scv_M_1('02') gets Neumos' shows for February
                 'twentyone': s[4], 'bands': s[5], 'tickets': s[6]} for s in filter(lambda x: type(x) == list, S) ]
    # 1                
    # Neumos
   
    def scv_1(self, date, br):
        month, day = self.splitDate(date) 
        soup = BeautifulSoup(br.open('http://neumos.com/neumoscalendar.php?month_offset=%s' % str(int(month) - int(NOW[1]))).read())
        calendar = soup.findAll('table')[1]
        calendar_dates = calendar.findAll('td')
        for d in calendar_dates:
            if self.search('\d+', d.renderContents()[0:5]) == day:
                entry = d
                break
        if len(entry.findAll('a')) > 0: 
            soup = BeautifulSoup(br.open('/%s' % entry.a['href']).read())
            return [self.parse_1(soup.find(attrs={'class': 'ShowParagraph'}), date)]
        else:
            return None # No <a> tag means there is no show that day

    def scv_M_1(self, month, br):
        shows = [ ]
        soup = BeautifulSoup(br.open('http://neumos.com/neumoscalendar.php?month_offset=%s' % str(int(month) - int(NOW[1]))).read())
        calendar = soup.findAll('table')[1]
        calendar_dates = calendar.findAll('td')
        for d in calendar_dates:
            if len(d.findAll('a')) > 0:
                soup = BeautifulSoup(br.open('/%s' % d.a['href']).read())
                break
        for d in soup.findAll(attrs={'class': 'ShowParagraph'}):
            if d.find(attrs={'class': 'date'}).renderContents()[4:7] == (months3[int(month) - 1]):
                shows.append(self.parse_1(d, month))
        return shows

    def parse_1(self, show, date):
        info = show.find(attrs={'class': 'description'})
        twentyOne = [False, True][info.renderContents().count('21+')] # 21+?
        t = info.find('a', href=re.compile(r'.*etix.com.*'))
        ticketsLink = t['href'] if t else ''

        if len(date) == 2:
            date += show.find(attrs={'class': 'date'}).renderContents().split('.')[2]

        bands = [a.renderContents() for a in info.findAll('a', attrs={'href': re.compile('neumos.php\?bandid.*')})]

        info = self.cleanText(info)

        price = self.search(r'\$\d+|Free', info)
        time = self.search(r'[\d:]+pm', info)
                     
        return [1, self.fullDate(date), time, price, twentyOne, bands, ticketsLink]

    # 8
    # 9
    # Showbox SoDo / Market

    def scv_M_8(self, month, br):
        return self.scv_M_showbox(month, br, 'sodo', 8)
    
    def scv_M_9(self, month, br):
        return self.scv_M_showbox(month, br, 'market', 9)

    def scv_M_showbox(self, month, br, vname, id):
        shows = [ ]
        urls = self.nav_showbox(month, br, vname)
        for u in urls:
            soup = BeautifulSoup(br.open('http://www.showboxonline.com%s' % u).read())
            shows.append(self.parse_showbox(soup.find(attrs={'class':re.compile(r'highlight-box.*')}), month, id))
        return shows

    def nav_showbox(self, month, br, vname, urls=[], no=1): # Recursive function to navigate Showbox's bullshit 10 shows per view website
        soup = BeautifulSoup(br.open('http://www.showboxonline.com/events.php?page=%s' % no).read())
        calendar_dates = soup.find(attrs={'class': 'alternating'}).findAll('li')
        for i, d in enumerate(calendar_dates):
            m = d.find(attrs={'class': 'date'}).renderContents()[0:4].strip()
            if m == months3[int(month) - 1] and self.search(vname, d.find(attrs={'class': 'venue'}).renderContents()):
                urls.append(d.find('a')['href'])
            if m == months3[int(month)]: # We have passed our desired month, stop the loop
                break
            if i == 9:
                self.nav_showbox(month, br, vname, urls, no + 1)
        return urls

    def parse_showbox(self, show, date, id):
        if len(date) == 2:
            d = self.search(r'\d+', self.search(r'\d+, %s' % NOW[0], show.find('strong', text='Day:').parent.parent.renderContents()))
            date += '%s%s' % (('0' if len(d) == 1 else ''), d)
        time = self.search(r'[\d:]+\spm', self.cleanText(show.find('strong', text='Doors open:').parent.parent))
        time = time[0:1 if time[1:4] == ':00' else 4] + 'pm'
        bands = [show.find(attrs={'class': 'nowrap'}).renderContents()]
        if show.find('strong', text='Advanced Ticket Prices*:'):
            price = '%sADV%sDAYOF' % (self.search(r'\$\d+', show.find('strong', text='Advanced Ticket Prices*:').parent.parent), 
                                      self.search(r'\$\d+', show.find('strong', text='Day of Show*:').parent.parent))
        else:
            price = self.search(r'\$\d+', show.find('strong', text='Ticket Prices*:').parent.parent)
        twentyOne = self.cleanText(show.find('strong', text='Ages:').parent.parent).find('21 & Over') > 0
        for a in show.findAll(attrs={'class': 'act'}):
            bands.append(a.renderContents())
        t = show.find('a', href=re.compile(r'.*tickets.*'))
        ticketsLink = self.search(r'.*showboxmarket', t['href']) if t else ''
        return [id, self.fullDate(date), time, price, twentyOne, bands, ticketsLink]
       
    # 16
    # Chop Suey

    def scv_16(self, date, br):
        m, d = self.splitDate(date)
        soup = BeautifulSoup(br.open('http://www.chopsuey.com/2012%' + '20%s.html' % date[0:2]).read()) # No fucking clue why their URL is structured this way but it is
        calendar = soup.find(attrs={'id': 'month'})
        for td in calendar('td'):
            try:
                if td.find(attrs={'class': 'date'}).renderContents() == str(d):
                    break
            except: pass
        return [self.parse_16(date, td)]

    def scv_M_16(self, month, br):
        shows = [ ]
        soup = BeautifulSoup(br.open('http://www.chopsuey.com/2012%' + '20%s.html' % month).read())
        calendar = soup.find(attrs={'id': 'month'})
        for td in calendar('td'):
            b = td.find(attrs={'class': 'bands'})
            if b and b.renderContents():
                date = self.parseDate(month, td.find(attrs={'class':'date'}).renderContents())
                shows.append(self.parse_16(date, td))
        return shows

    def parse_16(self, date, show):
        try:
            presents = show.find(attrs={'class':'presents'}).renderContents()
            if 'Komedy' in presents: return None # Sometimes there's this comedy group that does standup at Chop Suey. Catch this and ignore.
        except: pass
        t = show.find(attrs={'class':'time'}).renderContents()
        twentyOne = True if '21+' in t else False
        time = self.search('\d+pm', t)
        t = show.find(attrs={'class':'tix'})
        if t.find('a'):
            ticketsLink = t.find('a')['href']
        else:
            ticketsLink = None
        price = self.search('\$\w+', t.renderContents())
        if 'tba' in price:
            price = None
        elif 'adv' in price and price.count('$') == 1:
            price = self.search('\$\d+', price)
        bands = [show.find(attrs={'class':'headliner'}).renderContents()]
        for b in show.find(attrs={'class':'bands'}).renderContents().split('<br />'): # The way they format it is so wild and unpredictable, it would be best to just capture the raw text 
            bands.append(b)                                                           # and use a bottle-neck parser in the parent function for this shit. EX: 'w/' 'feat.' 'WITH' '[nothing]'
        bands = self.cleanList(bands)
        return [16, date, time, price, twentyOne, bands, ticketsLink] # Fuck.

    # 21
    # Tractor Tavern

    def scv_21(self, date, br):
        m, d = self.splitDate(date)
        soup = BeautifulSoup(br.open('http://www.tractortavern.com/calendar.asp?date=%s/3/2012' % m).read())
        calendar = soup.find(attrs={'id': 'Table4'})
        for td in calendar('td'):
            try:
                if td.font.b.renderContents() == str(d):
                    break
            except: pass
        print [self.parse_21(date, td)]

    def scv_M_21(self, month, br):
        shows = [ ]
        soup = BeautifulSoup(br.open('http://www.tractortavern.com/calendar.asp?date=%s/3/2012' % int(month)).read())
        calendar = soup.find(attrs={'id': 'Table4'})
        for td in calendar('td'):
            if td.find('font'):
                try:
                    date = self.parseDate(month, td.font.b.renderContents())
                    shows.append(self.parse_21(date, td))
                except: pass
        return shows

    def parse_21(self, date, show):
        time = self.search('[\d:]+pm', str(show.find('font', text=re.compile('Time:.*'))))
        price = self.search('\$[^~]*', str(show.find('font', text=re.compile('Charge:.*'))))
        ps = price.split('/')
        if len(ps) == 2:
            if 'adv' in ps[0] and 'dos' in ps[1]:
                ps = re.findall('\$\d+', price)
                price = '%sADV%sDAYOF' % (ps[0], ps[1])
        tL = show.find('font', text='Buy Tickets').parent.parent.parent
        ticketsLink = tL['href'] if tL else None
        bands = self.cleanList([re.search('[^a-z~\(\)]*', div.a.renderContents()).group(0).replace(' - ','') for div in show.findAll('div', attrs={'class': 'padding-item'})])
        return [21, date, time, price, True, bands, ticketsLink]
        

    # 24
    # Blue Moon Tavern

    def scv_24(self, date, br):
        soup = BeautifulSoup(br.open('http://bluemoonseattle.wordpress.com/').read())
        m, d = self.splitDate(date)
        entry = soup.find('span', text=re.compile(r'....%s\.%s' % (m, d))).parent.parent
        bands = entry.nextSibling.nextSibling.findAll('span')
        return [self.parse_24(date, entry, bands)]

    def scv_M_24(self, month, br):
        shows = [ ]
        soup = BeautifulSoup(br.open('http://bluemoonseattle.wordpress.com/').read())
        entries = [s.parent.parent for s in soup.findAll('span', text=re.compile(r'....%s\..*' % month))]
        bands = [s.nextSibling.nextSibling.findAll('span') for s in entries]
        for i, e in enumerate(entries):
            date = self.search(r'\d\d\.\d\d', e.span.renderContents()).replace('.','')
            shows.append(self.parse_24(date, e, bands[i]))
        return shows

    def parse_24(self, date, show, bands):
        price = None
        dayofweek = show.span.renderContents()[0:3]
        pms = re.search(r'\$\d+|FREE', show.renderContents() + ' '.join([b.renderContents() for b in bands]))
        if len(show.findAll('span')) == 1 or not pms:
            prices = {'THU': '$5', 'FRI': '$6', 'SAT': '$6', 'SUN': 'Free'}
            if dayofweek in prices:
                price = prices[dayofweek]
            else: pass
        if not price and pms:
            price = pms.group(0)
        else:
            price = None
        sT = re.search(r'[\d:]+\s?PM', show.renderContents() + ' '.join([b.renderContents() for b in bands]), re.I)
        times = {'THU': '9pm', 'FRI': '10pm', 'SAT': '10pm', 'SUN': '7pm'}
        if not sT and dayofweek in times:
            time = times[dayofweek]
        elif sT:
            time = sT.group(0)
        else:
            time = None
        return [24, self.fullDate(date), time, price, True, self.cleanList([b.findAll(text=True)[0] for b in bands]), None]
       
    # 30
    # Seamonster Lounge

    def scv_30(self, date, br):
        m, d = self.splitDate(date)
        soup = BeautifulSoup(br.open('http://www.seamonsterlounge.com/?page_id=22&month=%s&yr=2012' % ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec'][int(m) - 1]).read())
        for entry in soup.findAll(attrs={'class': 'day-with-date'}):
            if int(entry.span.renderContents()) == int(d):
                break
        return [self.parse_30(date, entry)]
    
    def scv_M_30(self, month, br):
        shows = [ ]
        soup = BeautifulSoup(br.open('http://www.seamonsterlounge.com/?page_id=22&month=%s&yr=2012' % ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec'][int(month) - 1]).read())
        for entry in soup.findAll(attrs={'class': 'day-with-date'}):
            shows.append(self.parse_30(self.parseDate(month, int(entry.span.renderContents())), entry))
        return shows

    def parse_30(self, date, show): # I've never been so nervous
        bands = [ ]
        times = [ ]
        for a in show('a'):
            heading = self.replaceMany(self.search(r'le">.*</span><strong>Time:</strong>\s?.*\s?pm\s?<b', str(a)), ['le">', '<strong>Time:</strong>', '<b']).split('</span>') # Such a hack, ugh I'm sorry
            bands.append(string.capitalize(heading[0]))
            times.append(heading[1])
        time = self.earliestTime(times)
        if 'MCTUFF TRIO' in bands:
            bands = ['McTuff Trio']
        
        return [30, date, time, 'Free', True, bands, None]
           
    # 40
    # Egan's Ballard Jamhouse

    def scv_40(self, date, br):
        m, d = self.splitDate(date)
        soup = BeautifulSoup(br.open('http://www.ballardjamhouse.com/schedule.html').read())
        for show in soup('dt'):
            if show.renderContents()[4:] == '%s %s' % (months3[m - 1], d):
                break
        show = show.parent
        dds = show.findAll('dd')
        if len(dds) > 1:
            result = [ ]
            for dd in dds:
                result.append([self.parse_40(date, dd)])
            return result
        else:
            return [self.parse_40(date, show.dd)]
    
    def scv_M_40(self, month, br):
        shows = [ ]
        soup = BeautifulSoup(br.open('http://www.ballardjamhouse.com/schedule.html').read())
        for show in soup('dt'):
            if show.renderContents()[4:7] == '%s' % months3[int(month) - 1]:
                d = show.renderContents()[4:].split(' ')
                date = self.parseDate(months3.index(d[0]) + 1, d[1])
                show = show.parent
                dds = show.findAll('dd')
                if len(dds) > 1:
                    result = [ ]
                    for dd in dds:
                        result.append(self.parse_40(date, dd))
                    shows.append(result)
                else:
                    shows.append(self.parse_40(date, show.dd))
        return shows

    def parse_40(self, date, show):
        rc = self.cleanText(show)        
        tL = show.findAll('a')
        ticketsLink = ''
        if self.search('ticket', rc):
            print 'ticket'
            for l in tL:
                if l.renderContents() != 'Website':
                    ticketsLink = l['href']
                    break
        time = self.search('\d+pm(\sand\s\d+pm)?', rc)
        price = self.search('\$\d+', rc) or 'Free'
        band = self.search('(?<=\s-\s).*', rc.replace(date, '')).split(', with')[0]
        return [40, date, time, price, False, band, ticketsLink or None]

    # 48
    # Cafe Racer
        
    def scv_48(self, date, br):      # So since Racer uses AJAX to change the month on their calendar we're gonna give them special treatment and call admin-ajax.php to get the data directly
        m, d = self.splitDate(date)  # because our poor little mechanize Browser doesn't do JS. This actually takes less time/code which is nice. Maybe we should try this method with other websites.

        
    def scv_M_48(self, month, br):
        soup = self.ajax_48(month)
        events = soup.findAll(attrs={'class': 'gce-tooltip-feed-1'}, text=re.compile(r'.*MUSIC:.*'))
        print events



    def ajax_48(self, m):
        return BeautifulSoup(urllib2.urlopen(
            'http://caferacerseattle.com/wp-admin/admin-ajax.php?action=gce_ajax&gce_type=page&gce_feed_ids=1&gce_title_text=&gce_widget_id=gce-page-grid-1&gce_max_events=0&gce_month=%s&gce_year=2012' % m
        ).read())

    





    def splitDate(self, date):
        return str(int(date[0:2])), str(int(date[2:4]))

    def fullDate(self, date):
        return '%s%s' % (date, '12' if len(date) == 4 else '')

    def cleanList(self, y):
        d = {}
        for x in y:
            if re.search('\w', x):
                d[x] = 1
        return [string.capitalize(x.strip()) for x in list(d.keys())]

    def clean(self, x):
        return ' '.join(self.cleanList(x.findAll(text=True)))

    def replaceMany(self, x, y):
        for r in y:
            x = x.replace(r, '')
        return x

    def earliestTime(self, x):
        conv = {}
        for t in x:
            a, b = t[:t.find('m')-1].split(':') if ':' in t else (t[:t.find('m')-1], 0)
            conv[(int(a) * 60) + int(b) - (720 if 'am' in t else 0)] = t
        return conv[min(conv.keys())].strip()
      
    def parseDate(self, month, day):
        month, day = str(month), str(day)
        month = '0' + month if len(month) == 1 else month
        day = '0' + day if len(day) == 1 else day
        return month+day

    def rid(self, phrase):
        orig = phrase
        for word in ['and', 'with', '&', ',', '<br>', '<br />', ' - ', ';', '\n']:
            while phrase.find(word) != -1:
                phrase = phrase.replace(word, 'xxxxx')
        if ':' in phrase:
            phrase = phrase.split(':')
            phrase = phrase[1]
        phrase = phrase.split('xxxxx')
        tR = []
        for i, p in enumerate(phrase):
            if p.lower() in ['sunday', 'saturday', 'friday', 'thursday', 'wednesday', 'tuesday', 'monday', 'special event', 'special guest', 'surprise guest'] or p == '':
               tR.append(p)
        for p in tR:
	csrfTOKEN = '{{ csrf_token }}';
            phrase.remove(p)

        for i, n in enumerate(phrase):
            phrase[i] = n.strip()
        return phrase    

          
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


class twitter(base):
    
    def random(self, type):
        regexes = {'exclaim': [r'&gt;\s(?P<r>.*\!)', r'\w[\w\d\s\?\.\,\'\-]+\!'], 'ask': [r'&gt;\s(?P<r>.*\?)', r'\w[\w\d\s\!\.\,\'\-]+\?'], 
                   'personal': [r'&gt;\s(?P<r>.*(\sme\s|I\s|\smy\s).*)', r'.*']}[type]
        br = self.freeBrowser()
        soup = BeautifulSoup(br.open('http://bash.org/?random').read())
        lines = soup.findAll('p', text=re.compile(regexes[0]))
        lines = [l.replace('&quot;', '"') for l in lines]
        goodlines = [ ]
        for l in lines:
            r = re.search(regexes[1], l, re.I)
            if r:
                goodlines.append(string.capwords(r.group(0)))
        return [re.search('(?<=(gt;\s|lt;\s)).*', x).group(0) for x in filter(lambda x: re.search('(?<=(gt;\s|lt;\s)).*', x), goodlines)]

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
        
    def tweet(self, tweet):
        self.twitter(['tweet', tweet])

