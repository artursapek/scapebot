# this is the file that runs on a crontab schedule to scrape all the venues

from scapebot import scapebot
from datetime import datetime

sc = scapebot()

scrapingFuncs = { 1: sc.scrapeVenue_neumos, 6: sc.scrapeVenue_STG, 7: sc.scrapeVenue_STG, 12: sc.scrapeVenue_STG,  26: sc.scrapeVenue_jazzAlley, 10: sc.scrapeVenue_crocodile }
STG = { 6: 'paramount', 7: 'moore', 12: 'neptune' }
daysMos = { '01': 31, '02': 29, '03': 31, '04': 30, '05': 31, '06': 30, '07': 31, '08': 31, '09': 30, '10': 31, '11': 30, '12': 31 }

now = datetime.now().month

global br
br = sc.freeBrowser()

def scrapeVenue(venue, month, br):
    if venue in STG:
        soup = scrapingFuncs[venue](br, venue=STG[venue], action='open', month=month)
    else:
        soup = scrapingFuncs[venue](br, action='open', month=month)
    for i in range(1, daysMos[month]):
        day = str(i)
        if i < 10:
            day = '0' + day
        date = month+day
        # nigger
        print date
       # try:
        if venue in STG:
            print scrapingFuncs[venue](br, date=date, soup=soup, venue=STG[venue])

        else:
            print scrapingFuncs[venue](date)
       # except:
        #    pass

def scrapeVenueDay(venue, date, br):
    soup = scrapingFuncs[venue](br, venue=STG[venue], action='open', month=date[0:2])
    if venue in STG:
        print scrapingFuncs[venue](br, date=date, soup=soup, venue=STG[venue])


scrapeVenue(12, '01', br)

#scrapeVenueDay(12, '0218', br)




