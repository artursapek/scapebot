# scapebot

scapebot is a web crawler dedicated to researching musicians and bands that come through Seattle.
I am also building functions to scrape venues' websites for show information.

required libraries: mechanize, BeautifulSoup

### band.research(name)

Researching the bands Avi Buffalo and LCD Soundsystem (~30 seconds):

```python
>>> from scapebot import band
>>> band = band()
>>> band.research('Avi Buffalo')
[u'Avi Buffalo', 'Southern rock / Twee pop', 'Long Beach', '']
>>> band.research('lcd soundsystem')
[u'LCD Soundsystem', 'Dance punk', 'NYC']
```

The return format is `[name, 1 or 2 genres, origin]`

When choosing genres scapebot compares a longer list he mines during the research and chooses the two most interesting ones based on the pool of options.
For example, given `['Disco', 'Italiodisco']` he will choose Italiodisco and ignore Disco because it's redundant. Given `['Folk', 'Rock']` he will choose only Folk and ignore Rock as it's a non-descriptive last resort genre.

### venue.scrape(venueID, MM[DD])

Collecting the shows at Neumos in February (~2 seconds):

```python
>>> from scapebot import venue
>>> venue = venue()
>>> venue.scrape(1, '02')
[[1, '020212', '8pm', '$7', True, [' Exohxo', " Let's Get Lost"], ''], [1, '020312', '8pm', '$10', False, [' Cool Nutz', ' Kung Foo Grip', ' E and Dae', ' Kingz of Kush', ' DJ Astronomar', ' Hosted By Grynch'], u'https://www.etix.com/ticket/online/performanceSearch.jsp?performance_id=1588813&cobrand=neumos'], [1, '020512', '6:30pm', '$16', False, [' Clinton Fearon & Mark Oi (Acoustic Set)', ' Live Wyya', ' Duane Stephenson', ' Adrian Xavier', ' The Escort Service', ' Alcyon Massive', ' Selecta Raiford'], u'https://www.etix.com/ticket/online/performanceSearch.jsp?performance_id=1588814&cobrand=neumos'], [1, '020812', '8pm', '$17', True, [' Dengue Fever', ' Secret Chiefs 3', ' U SCO'], u'https://www.etix.com/ticket/online/performanceSearch.jsp?performance_id=1583087&cobrand=neumos'], [1, '020912', '7pm', '$13', True, [' Staxx Brothers'], u'https://www.etix.com/ticket/online/performanceSearch.jsp?performance_id=1586030&cobrand=neumos'], [1, '021012', '7pm', '$10', True, [' The Freighms', ' Anchor The Tide', ' Step One', ' The Exchange'], u'https://www.etix.com/ticket/online/performanceSearch.jsp?performance_id=1601666&cobrand=neumos'], [1, '021112', '8pm', '$12', True, [' Tigerbeat', ' Radjaw'], u'https://www.etix.com/ticket/online/performanceSearch.jsp?performance_id=1591674&cobrand=neumos'], [1, '021512', '7pm', '$16', False, [' The Dear Hunter', ' Kay Kay and his Weathered Underground'], u'https://www.etix.com/ticket/online/performanceSearch.jsp?performance_id=1590628&cobrand=neumos'], [1, '021612', '8PM', '$8', True, [' SPORTS', ' The Fascination Movement', ' Tito Ramsey'], ''], [1, '021712', '8pm', '$15', True, [' Ume', ' Virgin Islands'], u'https://www.etix.com/ticket/online/performanceSearch.jsp?performance_id=1580521&cobrand=neumos'], [1, '021812', '8pm', '$13', True, [' VACATIONER'], u'https://www.etix.com/ticket/online/performanceSearch.jsp?performance_id=1579721&cobrand=neumos'], [1, '021912', '8pm', '$14', True, [], u'https://www.etix.com/ticket/online/performanceSearch.jsp?performance_id=1581316&cobrand=neumos'], [1, '022312', '8PM', '$8', True, [' The Pica Beats', ' Tomten'], u'https://www.etix.com/ticket/online/performanceSearch.jsp?performance_id=1603393&cobrand=neumos'], [1, '022412', '8PM', '$10', False, [' Bruce Leroy', ' Jarv Dee', ' DJ Swervewon'], u'https://www.etix.com/ticket/online/performanceSearch.jsp?performance_id=1601669&cobrand=neumos'], [1, '022612', '8pm', '$15', True, [], u'https://www.etix.com/ticket/online/performanceSearch.jsp?performance_id=1600905&cobrand=neumos'], [1, '022812', '7pm', '$15', False, [' Carnivores', ' Frank Broyles'], u'https://www.etix.com/ticket/online/performanceSearch.jsp?performance_id=1601333&cobrand=neumos']]
```
Format: `[venueID, date, time, price, 21+?, bands, ticket link if available]`
