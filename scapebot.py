' scapebot is a web spider that can research bands and scrape show information from Seattle venues '
' he is basically our slave '
' authors: Artur Sapek, Michael Beswetherick '

from BeautifulSoup import BeautifulSoup
from mechanize import Browser
from collections import defaultdict
from datetime import datetime
from django.utils import simplejson
try: from main.models import *
except: pass
try: from PIL import Image as img
except: pass
from random import *
import csv
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

    def sanitize(self, x):
        for i in range(1, 32):
            x = ''.join(x.split(str(string.punctuation)[i]))
        return x

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
        print bandname, forceLocal
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
    
    def research(self, bandname, save = False, forceLocal = False, ignoreSuggest = False, sources = {}):
        nameFormatted = False
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

        print sourceURLS

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
                print URL
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
                print URL
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
                        print 'lastm'
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
                    print 'sc'
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
                    print 'fb'

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

        print sources

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
            band = Band.objects.filter(bandname__iexact=choice)
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
            return [band.id, band.bandname, g, o, c]
        else:
            band.genre = genre if genre != None else g
            band.origin = origin if origin != None else o
            band.cover = cover if cover != None else c
            band.save()
            return [band.id, band.bandname, band.genre, band.origin, band.cover]

    def cover(self, choice, src=None): # swag
        print choice, src
        br = self.freeBrowser()
        if not choice:
            return None
        band = self.get(choice)        
#        if not os.path.exists('main/static/img/covers/%s/%s__.jpg' % (bandname.lower().replace('the ', '')[0], ''.join(re.findall('\w', bandname)).lower()) ):
        if not src:
            breakNow = False
            albumsRepo = { }
            result = [ ]
            albumSRC = ''
            URL = filter(lambda f: '/' + band.bandname.lower().replace(' ', '-') + '/' in f, self.GoogleAPI(band.bandname, '014750848680997063315:uwrdxv39alm'))[0]
            print URL
            if URL:
                soup = BeautifulSoup(br.open(URL).read())
                if re.search(self.regexify(band.bandname), soup.h1.renderContents(), re.I):
                    albums = soup.findAll('img', attrs={'class': 'artwork'})
                    for a in albums:
                        if a['src'].find('/Music/') > -1:
                            albumSoup = BeautifulSoup(br.open(a.parent.parent['href']).read())
                            release = albumSoup.find('li', attrs={'class': 'release-date'})
                            # Ignore non-albums (reprises, singles, reissues)
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
            cover.save('/home/bandscape/dev/bandscape/main/static/img/covers/%s/%s.jpg' % (band.bandname.lower().replace('the ', '')[0], ''.join(re.findall('\w', band.bandname)).lower()), "JPEG", quality=90) 
            cover.thumbnail( ( 60, 60), img.ANTIALIAS)
            cover.save('/home/bandscape/dev/bandscape/main/static/img/covers/%s/%s__.jpg' % (band.bandname.lower().replace('the ', '')[0], ''.join(re.findall('\w', band.bandname)).lower()), "JPEG", quality=90) 
            return



# ----

    def freeBrowser(self):
        br = Browser()
        br.set_handle_robots(False)
        br.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.202 Safari/535.1')]
        return br

# ----




    # Scraping functions begin here!


    # All venues have functions for A) Specific date and B) Upcoming future if their homepage is formatted that way (EX: Neumos's). The latter is for efficiency and to leave as small a footprint as possible 
    # Format: [ showID, venueID, Date, Time, Price, 21+, Bands ]



    #pre: pass in a date in ddmmyy fashion :)
    #post: returns a list of information on the show

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
            phrase.remove(p)

        for i, n in enumerate(phrase):
            phrase[i] = n.strip()
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
                    if not re.search(r'free.*tour', goToShow.renderContents(), re.I) and not re.search(r'special event', goToShow.renderContents(), re.I):
                        bands.append(goToShow.renderContents())
                        #go to next page to find 21+ & price
                        linkText = goToShow.renderContents()
                        if linkText.find('&amp;'):
                            linkText = linkText[:linkText.find('&amp;')]
                        soup = BeautifulSoup(br.follow_link(text_regex = linkText).read())
                        guests = soup.find(attrs={'id': 'aGuest'})
                        if guests:
                            guests = self.rid(guests.renderContents().replace('<br>', '').replace('\n', ''))
                        if guests: bands += guests
                        #do price
                        price = soup.find(attrs={'class' : 'aPrice'})
                        parsedPrice = [ ] 
                        if price:
                            price = price.renderContents()
                            dict = None
                            priceItems = re.findall(r'\$[/\$\w\s]+', price)
                            for i,x in enumerate(priceItems):
                                y = re.findall('\$[\w\s]+', x)
                                if len(y) > 1: # if two prices in one line nigguh
                                    yjoined = ''.join(y)
                                    if yjoined.find('UW') != -1: UW = True
                                    else: UW = False
                                    if UW:
                                        ints = re.findall('\d+', yjoined)
                                        for intInd, intN in enumerate(ints):
                                            ints[intInd] = int(intN)
                                        minPrice = min(ints)
                                        maxPrice = max(ints)
                                        parsedPrice.append('$%s%s(UW)' % (str(maxPrice), str(minPrice)))
                                        if re.search('advance', yjoined):
                                            parsedPrice.append('ADV')
                                        if re.search('day of', yjoined):
                                            parsedPrice.append('DAYOF')
                                elif len(y) == 1:
                                    parsedPrice.append(re.search(r'\$\w+', y[0]).group(0))
                                    if re.search('advance', x, re.I):
                                        parsedPrice[i] += 'ADV'
                                    if re.search('uw student', x, re.I):
                                        parsedPrice[i] += '(UW)'
                                    if re.search('day of show', x, re.I):
                                        parsedPrice[i] += 'DAYOF'
                            result.append(''.join(parsedPrice))
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
                        br.back()
                        result.append(bands)
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

    def parseDate(self, month, day):
        day = str(day)
        if len(day) == 1:
            day = '0' + day
        return month+day


    def scrapeVenue_fullMonth(self, venue, month):
        br = self.freeBrowser()
        scrapingFuncs = { 1: self.scrapeVenue_neumos, 6: self.scrapeVenue_STG, 7: self.scrapeVenue_STG, 12: self.scrapeVenue_STG,  26: self.scrapeVenue_jazzAlley, 10: self.scrapeVenue_crocodile }
        STG = { 6: 'paramount', 7: 'moore', 12: 'neptune' }
        daysMos = { '01': 31, '02': 29, '03': 31, '04': 30, '05': 31, '06': 30, '07': 31, '08': 31, '09': 30, '10': 31, '11': 30, '12': 31 }
        shows = [ ]
        soup = scrapingFuncs[venue](br, venue=STG[venue] if venue in STG else venue, action='open', month=month)
        for i in range(1, daysMos[month]):
            date = self.parseDate(month, i)
            show = scrapingFuncs[venue](br, date=date, soup=soup, venue=STG[venue] if venue in STG else venue)
            if show:
                    shows.append(show)
        print shows
        self.addShows(shows, venue) # chain into the next part which adds em

    def addShows(self, shows, venue):
        for index, show in enumerate(shows):
            # first check to see if we already have it
            alreadyHaveit = Show.objects.filter(venue=venue, date=show[0])
            if not alreadyHaveit:
                appendedInfo = ''
                bands = show[4]
                newBands = []
                for i, b in enumerate(bands):
                    found = False
                    iterations = self.rBQueries(b)
                    for y, x in enumerate(iterations): # first check all iterations to see if they be chillin in our DB
                        s = searchDB = Band.objects.filter(bandname=x)
                        if len(searchDB) == 1: # if we've found ONE match for the name
                            newBands.append(searchDB[0].id) # replace that bandname with the ID it has in our DB
                            found = True
                            if y > 0:
                                appendedInfo += '%s:%s' % (str(y), iterations[0].replace(s[0],'')) # add the extra info to the show so we can display it with the artist :)
                            break
                    if not found:
                        for y, x in enumerate(iterations): # when we haven't found it we fucking scrape it
                            print x
                            s = scrapeIt = self.researchBand(x)
                            if scrapeIt:
                                searchDB = Band.objects.filter(bandname=scrapeIt[0])
                                if len(searchDB) == 1:
                                    newBands.append(searchDB[0].id) # replace that bandname with the ID it has in our DB
                                    found = True
                                    if y > 0:
                                        appendedInfo += '%s:%s' % (str(y), iterations[0].replace(s[0],'')) # add the extra info to the show so we can display it with the artist :)
                                    break
                                else:
                                    newBand = Band(bandname=s[0], genre=s[1], origin=s[2])
                                    newBand.save()
                                    newBands.append(newBand.id)
                                    if y > 0:
                                        appendedInfo += '%s:%s' % (str(y), iterations[0].replace(s[0],'')) # add the extra info to the show so we can display it with the artist :)
                                    found = True
                                    break
                if newBands: # if we found any or all bands (usually it was all or none)
                    for FUCK, YOU in enumerate(newBands):
                        newBands[FUCK] = str(YOU)
                    newShow = Show(venue = venue, date=show[0]+'12', time=show[1], price=show[2], twentyone=show[3], bands=','.join(newBands), bandnameow=appendedInfo if appendedInfo else '')
                    newShow.save()
                    print newShow

    def rBQueries(self, query):
        queries = [ query ]
        for x in [' with ', ' & ', ' and ', ' - ', ': ']:
            find = query.find(x)
            if find > -1:
                queries.append(query[:find].strip())
        return queries
     

