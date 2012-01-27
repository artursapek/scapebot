# scapebot

scapebot is a web crawler dedicated to researching musicians and bands that come through Seattle.

**REQUIRES**: mechanize, BeautifulSoup

For the time being the main function available to the public is `band.research()` which returns information about a band/musician given a name.
The return format is `[ formatted name, 1 or 2 genres, origin, source of their music(incomplete) ]`

```python
>>> from scapebot import band
>>> band = band()
>>> band.research('Avi Buffalo')
[u'Avi Buffalo', 'Southern rock / Twee pop', 'Long Beach', '']
>>> band.research('lcd soundsystem')
[u'LCD Soundsystem', 'Dance punk', 'NYC', '']
```

For smaller less popular Seattle bands you can use the optional `forceLocal` argument which simply makes the script prefer Seattle-related results.

```python
>>> band.research('lost dogma', forceLocal=True)
[u'LOST DOGMA', 'Country / Americana', 'Seattle', '']
```

When choosing genres scapebot compares a longer list he mines during the research and chooses the two most interesting ones based on the pool of options.

For example, given `['Disco', 'Italiodisco']` he will choose Italiodisco and ignore Disco because it's redundant. Given `['Folk', 'Rock']` he will choose only Folk and ignore Rock as it's a non-descriptive last resort genre.

Please keep in mind that scapebot is still very much a work in progress.
