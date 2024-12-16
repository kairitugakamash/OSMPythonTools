# https://pypi.org/project/OSMPythonTools/

pip install OSMPythonTools

# ================ Example 1 ==================
# Which object does the way with the ID 5887599 represent?

from OSMPythonTools.api import Api
api = Api()
way = api.query('way/5887599')

way.tag('building')
# 'castle'
way.tag('architect')
# 'Johann Lucas von Hildebrandt'
way.tag('website')
# 'http://www.belvedere.at'

# ================ Example 2 ==================
# What is the English name of the church called ‘Stephansdom’, what address does it have, and which of which denomination is the church?
from OSMPythonTools.overpass import Overpass
overpass = Overpass()
result = overpass.query('way["name"="Stephansdom"]; out body;')

# This time, the result is a number of objects, which can be accessed by result.elements(). We just pick the first one:
stephansdom = result.elements()[0]

stephansdom.tag('name:en')
# "Saint Stephen's Cathedral"
'%s %s, %s %s' % (stephansdom.tag('addr:street'), stephansdom.tag('addr:housenumber'), stephansdom.tag('addr:postcode'), stephansdom.tag('addr:city'))
# 'Stephansplatz 3, 1010 Wien'
stephansdom.tag('building')
# 'cathedral'
stephansdom.tag('denomination')
# 'catholic'

# ================ Example 3 ==================
# How many trees are in the OSM data of Vienna? And how many trees have there been in 2013?
from OSMPythonTools.nominatim import Nominatim
nominatim = Nominatim()
areaId = nominatim.query('Vienna, Austria').areaId()

# This area ID can now be used to build the corresponding query:
from OSMPythonTools.overpass import overpassQueryBuilder, Overpass
overpass = Overpass()
query = overpassQueryBuilder(area=areaId, elementType='node', selector='"natural"="tree"', out='count')
result = overpass.query(query)
result.countElements()

# There are 134520 trees in the current OSM data of Vienna. How many have there been in 2013?
result = overpass.query(query, date='2013-01-01T00:00:00Z', timeout=60)
result.countElements()


# ================ Example 4 ==================
# Where are waterbodies located in Vienna?
from OSMPythonTools.nominatim import Nominatim
nominatim = Nominatim()
areaId = nominatim.query('Vienna, Austria').areaId()

# The query can be built like in the examples before. 
# This time, however, the argument includeGeometry=True is provided to the overpassQueryBuilder in order to let him generate a query that downloads the geometry data.

from OSMPythonTools.overpass import overpassQueryBuilder, Overpass
overpass = Overpass()
query = overpassQueryBuilder(area=areaId, elementType=['way', 'relation'], selector='"natural"="water"', includeGeometry=True)
result = overpass.query(query)

# Next, we can exemplarily choose one random waterbody (the first one of the download ones) and compute its geometry like follows:

firstElement = result.elements()[0]
firstElement.geometry()
# {"coordinates": [[[16.498671, 48.27628], [16.4991, 48.276345], ... ]], "type": "Polygon"}

# Observe that the resulting geometry is provided in the GeoJSON format.
# https://en.wikipedia.org/wiki/GeoJSON

# ================ Example 5 ==================
# How did the number of trees in Berlin, Paris, and Vienna change over time?

from collections import OrderedDict
from OSMPythonTools.data import Data, dictRangeYears, ALL
from OSMPythonTools.overpass import overpassQueryBuilder, Overpass

# The question has two ‘dimensions’: the dimension of time, and the dimension of different cities:

dimensions = OrderedDict([
    ('year', dictRangeYears(2013, 2017.5, 1)),
    ('city', OrderedDict({
        'berlin': 'Berlin, Germany',
        'paris': 'Paris, France',
        'vienna': 'Vienna, Austria',
    })),
])

# We have to define how we fetch the data. We again use Nominatim and the Overpass API to query the data (it can take some time to perform this query the first time!):

overpass = Overpass()
def fetch(year, city):
    areaId = nominatim.query(city).areaId()
    query = overpassQueryBuilder(area=areaId, elementType='node', selector='"natural"="tree"', out='count')
    return overpass.query(query, date=year, timeout=60).countElements()
data = Data(fetch, dimensions)

# We can now easily generate a plot from the result:
data.plot(city=ALL, filename='example4.png')

# Alternatively, we can generate a table from the result

data.select(city=ALL).getCSV()

# MORE ON osmpythontools
# OSMPythonTools.Api - Access to the official OSM API -- https://pypi.org/project/OSMPythonTools/docs/api.md
# OSMPythonTools.Data - Collecting, mining, and drawing data from OSM; to be used in combination with the other modules -- https://pypi.org/project/OSMPythonTools/docs/data.md
# OSMPythonTools.Element - Elements are returned by other services, like the OSM API or the Overpass API -- https://pypi.org/project/OSMPythonTools/docs/element.md
# OSMPythonTools.Nominatim - Access to Nominatim, a reverse geocoder -- https://pypi.org/project/OSMPythonTools/docs/nominatim.md
# OSMPythonTools.Overpass - Access to the Overpass API -- https://pypi.org/project/OSMPythonTools/docs/overpass.md


# LOGGING
import logging
logging.getLogger('OSMPythonTools').setLevel(logging.ERROR)

# TESTS
pip install OSMPythonTools [test]
pytest --verbose
