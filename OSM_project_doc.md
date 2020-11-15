# Open Street Map Data Wrangling

## Map Area

The map area consists of Richmond, Rosenberg and Sugar Land, TX. This is the area where I currently live, so I am familiar with the data being examined.

https://www.openstreetmap.org/export#map=13/29.5959/-95.7038

## Problems Encountered in the Dataset
<ul>
<li>Inconsistent street types</li>
<li>Incosisttent street names</li>
<li>Incosistent names for keys</li>
</ul>

### Inconsistent street types
<p>Running the audit.py script from the case study revealed that several street types were inconsistant in their use of abbreviations. The following values were ignored and accepted as correct:</p>


```python
 ["Street", "Avenue", "Boulevard", "Drive", "Lane", "Road", "Parkway", "Freeway", "Way", "Court", "Crossing", "Circle", "Walk"]
```

<p>The remaining values returned were the following:</p>


```python
{'1092': {'FM 1092'},
'1464': {'FM 1464'},
'1640': {'FM 1640'},
'200': {'E Hwy 90 Alt #200'},
'285': {'Southwest Fwy #285'},
'300': {'Southwest Freeway, Ste 300'},
'359': {'FM 359', 'Farm to market 359', 'Fm 359', 'Farm to Market 359'},
'36': {'TX 36'},
'59': {'Southwest Freeway 59'},
'6': {'Highway 6', S Highway 6', 'S Hwy 6', 'State Highway 6', 'TX 6', 'Texas Highway 6'},
'77478': {'3412 Hwy 6, Sugar Land, TX 77478'},
'90': {'Highway 90'},
'90A': {'US 90A', 'Highway 90A', 'Hwy 90A'},
'90a': {'Hwy 90a'},
'Alt': {'E Hwy 90 Alt'},
'Bellfort': {'West Bellfort'},
'Blvd': {'W Airport Blvd', 'University Blvd', 'Sweetwater Blvd'},      
'Cir': {'Eugene Heimann Cir'},
'E': {'Avenue E'},
'Fm1640': {'Fm1640'},
'Fm359': {'Fm359'},
'Fwy': {'Southwest Fwy'},
'H': {'Avenue H'},
'N': {'Avenue N'},
'North': {'Town Center Boulevard North'},
'Place': {'Austins Place'},
'South': {'Highway 6 South', 'West Grand Parkway South', 'West Sam Houston Parkway South'},
'St': {'liberty St'},
'T2008': {'Southwest Fwy Ste T2008'},
'pkwy': {'Grand pkwy'},
'road': {'FM 762 road'}
     }
```

<p>"clean_st_type.py" uses the update_name function with the following dictionary to convert the abbreviated street to consistent full words within the shape_element function in data.py:</p>


```python
mapping = { "St": "Street",
            "Rd": "Road",
            "Cir": "Circle",
            "Blvd": "Boulevard",
            "Fwy": "Freeway"
            "pkwy": "Parkway"
            }
```

### Inconsistent Street Names
<p>Examination of the audit.py results show several roadways being referred to in various ways (i.e., Highway 90A, US 90A and Hwy 90A all refer to US Highway 90 Alt). "clean_st_name.py" updates these in a similar fashion as "clean_st_type.py" with the st_mapping dictionary.</p>


```python
st_mapping = { 
    '1092': "Farm to Market 1092",
    '1464': "Farm to Market 1464",
    '1640': "Farm to Market 1640",
    '200': "East US Highway 90 Alt",
    '285': "Southwest Freeway",
    '300': "Southwest Freeway",
    '359': "Farm to Market 359",
    '36': "TX Highway 36",
    '59': "Southwest Freeway",
    '6': "TX Highway 6",
    '77478': "TX Highway 6",
    '90': "US Highway 90", 
    '90A': "US Highway 90 Alt",
    '90a': "US Highway 90 Alt",
    'Alt': "East US Highway 90 Alt", 
    'Fm1640': "Farm to Market 1640",
    'Fm359': "Farm to Market 359",
    'T2008': "Southwest Freeway",
    'road': "Farm to Market 762"
    }
```

### Inconsistent Key Names
<p>Further review of the data found that the keys for county names were listed as both "county" and "county_name". The update_key function from clean_key.py was added to the shape_element function in data.py to map all to "county_name" as the underscore format is consistant with the naming convention seen in other key types.</p> 


```python
mapping = { "county": "county_name" }
```

## Data Overview


```python
import os
import pandas as pd
import sqlite3

conn = sqlite3.connect("sugarroserich.db")
cur = conn.cursor()
```

### File Sizes


```python
print ("File Sizes:")
print ("nodes.csv: " + str(os.stat('nodes.csv').st_size/1000000) + " MB")
print ("nodes_tags.csv: " + str(os.stat('nodes_tags.csv').st_size/1000000) + " MB")
print ("ways.csv: " + str(os.stat('ways.csv').st_size/1000000) + " MB")
print ("ways_tags.csv: " + str(os.stat('ways_tags.csv').st_size/1000000) + " MB")
print ("ways_nodes.csv: " + str(os.stat('ways_nodes.csv').st_size/1000000) + " MB")
print ("sugarroserich.osm: " + str(os.stat('sugarroserich.osm').st_size/1000000) + " MB")
print ("sugarroserich.db: " + str(os.stat('sugarroserich.db').st_size/1000000) + " MB")
```

    File Sizes:
    nodes.csv: 41.895342 MB
    nodes_tags.csv: 0.610251 MB
    ways.csv: 3.503205 MB
    ways_tags.csv: 5.989224 MB
    ways_nodes.csv: 14.452834 MB
    sugarroserich.osm: 108.103162 MB
    sugarroserich.db: 79.777792 MB
    

### Number of Nodes


```python
df_nodes = pd.read_sql_query("SELECT COUNT(*) AS '# of nodes' FROM nodes;", conn)
df_nodes
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th># of nodes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>493516</td>
    </tr>
  </tbody>
</table>
</div>



### Number of Ways


```python
df_ways = pd.read_sql_query("SELECT COUNT(*) AS '# of ways' FROM ways;", conn)
df_ways
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th># of ways</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>57394</td>
    </tr>
  </tbody>
</table>
</div>



### Number of Unique Users


```python
df_users = pd.read_sql_query("SELECT COUNT(DISTINCT(uid)) AS '# of users' FROM (SELECT uid FROM nodes UNION ALL SELECT uid FROM ways);", conn)
df_users
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th># of users</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>808</td>
    </tr>
  </tbody>
</table>
</div>



### Number of Area Leisure Options


```python
df_liesure = pd.read_sql_query("SELECT value AS 'Leisure Nodes', COUNT(value) AS 'Total' FROM nodes_tags WHERE key == 'leisure' GROUP BY value;", conn)
df_liesure
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Leisure Nodes</th>
      <th>Total</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>bleachers</td>
      <td>11</td>
    </tr>
    <tr>
      <th>1</th>
      <td>fitness_centre</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>fitness_station</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3</th>
      <td>garden</td>
      <td>4</td>
    </tr>
    <tr>
      <th>4</th>
      <td>ice_rink</td>
      <td>1</td>
    </tr>
    <tr>
      <th>5</th>
      <td>park</td>
      <td>9</td>
    </tr>
    <tr>
      <th>6</th>
      <td>picnic_table</td>
      <td>16</td>
    </tr>
    <tr>
      <th>7</th>
      <td>playground</td>
      <td>10</td>
    </tr>
    <tr>
      <th>8</th>
      <td>sports_centre</td>
      <td>4</td>
    </tr>
    <tr>
      <th>9</th>
      <td>swimming_pool</td>
      <td>4</td>
    </tr>
  </tbody>
</table>
</div>



### Area Dining Options


```python
df_food = pd.read_sql_query("SELECT a.value AS 'Service Type', b.value AS 'Cuisine', COUNT(b.value) AS 'Total' FROM (SELECT * FROM nodes_tags WHERE value IN ('restaurant', 'cafe', 'fast_food')) a JOIN (SELECT * FROM nodes_tags WHERE key == 'cuisine') b ON a.id = b.id GROUP BY b.value ORDER BY a.value;", conn)
df_food
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Service Type</th>
      <th>Cuisine</th>
      <th>Total</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>cafe</td>
      <td>coffee_shop</td>
      <td>4</td>
    </tr>
    <tr>
      <th>1</th>
      <td>cafe</td>
      <td>coffee_shop;sandwich</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>cafe</td>
      <td>donut</td>
      <td>2</td>
    </tr>
    <tr>
      <th>3</th>
      <td>fast_food</td>
      <td>burger</td>
      <td>15</td>
    </tr>
    <tr>
      <th>4</th>
      <td>fast_food</td>
      <td>chicken</td>
      <td>2</td>
    </tr>
    <tr>
      <th>5</th>
      <td>fast_food</td>
      <td>chinese</td>
      <td>2</td>
    </tr>
    <tr>
      <th>6</th>
      <td>fast_food</td>
      <td>ice_cream;burger</td>
      <td>1</td>
    </tr>
    <tr>
      <th>7</th>
      <td>fast_food</td>
      <td>italian</td>
      <td>1</td>
    </tr>
    <tr>
      <th>8</th>
      <td>fast_food</td>
      <td>juice</td>
      <td>1</td>
    </tr>
    <tr>
      <th>9</th>
      <td>fast_food</td>
      <td>mexican</td>
      <td>7</td>
    </tr>
    <tr>
      <th>10</th>
      <td>fast_food</td>
      <td>pizza</td>
      <td>8</td>
    </tr>
    <tr>
      <th>11</th>
      <td>fast_food</td>
      <td>sandwich</td>
      <td>8</td>
    </tr>
    <tr>
      <th>12</th>
      <td>restaurant</td>
      <td>american</td>
      <td>5</td>
    </tr>
    <tr>
      <th>13</th>
      <td>restaurant</td>
      <td>asian</td>
      <td>3</td>
    </tr>
    <tr>
      <th>14</th>
      <td>restaurant</td>
      <td>barbecue</td>
      <td>2</td>
    </tr>
    <tr>
      <th>15</th>
      <td>restaurant</td>
      <td>indian</td>
      <td>2</td>
    </tr>
    <tr>
      <th>16</th>
      <td>restaurant</td>
      <td>japanese</td>
      <td>1</td>
    </tr>
    <tr>
      <th>17</th>
      <td>restaurant</td>
      <td>mediterranean</td>
      <td>1</td>
    </tr>
    <tr>
      <th>18</th>
      <td>restaurant</td>
      <td>mediterranean;buffet</td>
      <td>1</td>
    </tr>
    <tr>
      <th>19</th>
      <td>restaurant</td>
      <td>pizza;buffet</td>
      <td>1</td>
    </tr>
    <tr>
      <th>20</th>
      <td>restaurant</td>
      <td>regional</td>
      <td>2</td>
    </tr>
    <tr>
      <th>21</th>
      <td>restaurant</td>
      <td>seafood</td>
      <td>2</td>
    </tr>
    <tr>
      <th>22</th>
      <td>restaurant</td>
      <td>sushi</td>
      <td>1</td>
    </tr>
    <tr>
      <th>23</th>
      <td>restaurant</td>
      <td>tex-mex</td>
      <td>5</td>
    </tr>
    <tr>
      <th>24</th>
      <td>restaurant</td>
      <td>vietnamese</td>
      <td>1</td>
    </tr>
    <tr>
      <th>25</th>
      <td>restaurant</td>
      <td>vietnamese;chinese</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>



## Additional Ideas

<p>I believe that further examination could be done to the way that places are categorized and how they are designated as either hamlet, town or city. The following query shows the breakdown for this area:</p>


```python
df_places = pd.read_sql_query("WITH tags AS (SELECT * FROM nodes_tags UNION ALL SELECT * FROM ways_tags) SELECT e.id, e.key, e.value, m.value AS place FROM (SELECT * FROM tags WHERE key == 'name') e JOIN (SELECT * FROM tags WHERE key == 'place') m ON  e.id = m.id ORDER BY place ;", conn)
df_places
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id</th>
      <th>key</th>
      <th>value</th>
      <th>place</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>151413262</td>
      <td>name</td>
      <td>Sugar Land</td>
      <td>city</td>
    </tr>
    <tr>
      <th>1</th>
      <td>316998162</td>
      <td>name</td>
      <td>Fort Bend</td>
      <td>county</td>
    </tr>
    <tr>
      <th>2</th>
      <td>151340813</td>
      <td>name</td>
      <td>Town West</td>
      <td>hamlet</td>
    </tr>
    <tr>
      <th>3</th>
      <td>151383271</td>
      <td>name</td>
      <td>Pecan Grove</td>
      <td>hamlet</td>
    </tr>
    <tr>
      <th>4</th>
      <td>151416096</td>
      <td>name</td>
      <td>Herbert</td>
      <td>hamlet</td>
    </tr>
    <tr>
      <th>5</th>
      <td>151474893</td>
      <td>name</td>
      <td>Four Corners</td>
      <td>hamlet</td>
    </tr>
    <tr>
      <th>6</th>
      <td>151493639</td>
      <td>name</td>
      <td>Crabb</td>
      <td>hamlet</td>
    </tr>
    <tr>
      <th>7</th>
      <td>151539046</td>
      <td>name</td>
      <td>First Colony</td>
      <td>hamlet</td>
    </tr>
    <tr>
      <th>8</th>
      <td>151655778</td>
      <td>name</td>
      <td>Fifth Street</td>
      <td>hamlet</td>
    </tr>
    <tr>
      <th>9</th>
      <td>151713038</td>
      <td>name</td>
      <td>Booth</td>
      <td>hamlet</td>
    </tr>
    <tr>
      <th>10</th>
      <td>151750067</td>
      <td>name</td>
      <td>Paynes</td>
      <td>hamlet</td>
    </tr>
    <tr>
      <th>11</th>
      <td>151878287</td>
      <td>name</td>
      <td>Dewalt</td>
      <td>hamlet</td>
    </tr>
    <tr>
      <th>12</th>
      <td>151878428</td>
      <td>name</td>
      <td>McHattie</td>
      <td>hamlet</td>
    </tr>
    <tr>
      <th>13</th>
      <td>151907675</td>
      <td>name</td>
      <td>Foster</td>
      <td>hamlet</td>
    </tr>
    <tr>
      <th>14</th>
      <td>151959488</td>
      <td>name</td>
      <td>Cumings</td>
      <td>hamlet</td>
    </tr>
    <tr>
      <th>15</th>
      <td>151406735</td>
      <td>name</td>
      <td>New Territory</td>
      <td>neighbourhood</td>
    </tr>
    <tr>
      <th>16</th>
      <td>151479781</td>
      <td>name</td>
      <td>Greatwood</td>
      <td>neighbourhood</td>
    </tr>
    <tr>
      <th>17</th>
      <td>1970719460</td>
      <td>name</td>
      <td>Del Webb Sweetgrass</td>
      <td>neighbourhood</td>
    </tr>
    <tr>
      <th>18</th>
      <td>3833672007</td>
      <td>name</td>
      <td>Old Orchard</td>
      <td>neighbourhood</td>
    </tr>
    <tr>
      <th>19</th>
      <td>3833672008</td>
      <td>name</td>
      <td>Orchard Lakes</td>
      <td>neighbourhood</td>
    </tr>
    <tr>
      <th>20</th>
      <td>3833672009</td>
      <td>name</td>
      <td>Stratford Park</td>
      <td>neighbourhood</td>
    </tr>
    <tr>
      <th>21</th>
      <td>3833672010</td>
      <td>name</td>
      <td>Summerfield</td>
      <td>neighbourhood</td>
    </tr>
    <tr>
      <th>22</th>
      <td>3833675658</td>
      <td>name</td>
      <td>Pheasant Creek</td>
      <td>neighbourhood</td>
    </tr>
    <tr>
      <th>23</th>
      <td>3833675659</td>
      <td>name</td>
      <td>Shiloh Lake Estates</td>
      <td>neighbourhood</td>
    </tr>
    <tr>
      <th>24</th>
      <td>3889455314</td>
      <td>name</td>
      <td>Kingdom Heights</td>
      <td>neighbourhood</td>
    </tr>
    <tr>
      <th>25</th>
      <td>3889684398</td>
      <td>name</td>
      <td>Fairpark Village</td>
      <td>neighbourhood</td>
    </tr>
    <tr>
      <th>26</th>
      <td>3889884096</td>
      <td>name</td>
      <td>Walnut Creek</td>
      <td>neighbourhood</td>
    </tr>
    <tr>
      <th>27</th>
      <td>4030182646</td>
      <td>name</td>
      <td>Grand Vista</td>
      <td>neighbourhood</td>
    </tr>
    <tr>
      <th>28</th>
      <td>4119703301</td>
      <td>name</td>
      <td>Briscoe Falls</td>
      <td>neighbourhood</td>
    </tr>
    <tr>
      <th>29</th>
      <td>6016904765</td>
      <td>name</td>
      <td>Brazos Ranch Apartment Homes</td>
      <td>neighbourhood</td>
    </tr>
    <tr>
      <th>30</th>
      <td>6016933935</td>
      <td>name</td>
      <td>Dolce Living Rosenberg Apartment Homes</td>
      <td>neighbourhood</td>
    </tr>
    <tr>
      <th>31</th>
      <td>191950479</td>
      <td>name</td>
      <td>Keegans Glen</td>
      <td>neighbourhood</td>
    </tr>
    <tr>
      <th>32</th>
      <td>191955172</td>
      <td>name</td>
      <td>Huntington Village</td>
      <td>neighbourhood</td>
    </tr>
    <tr>
      <th>33</th>
      <td>191958308</td>
      <td>name</td>
      <td>Meadow Park</td>
      <td>neighbourhood</td>
    </tr>
    <tr>
      <th>34</th>
      <td>191963198</td>
      <td>name</td>
      <td>Bayou Place</td>
      <td>neighbourhood</td>
    </tr>
    <tr>
      <th>35</th>
      <td>191963199</td>
      <td>name</td>
      <td>Parkglen West</td>
      <td>neighbourhood</td>
    </tr>
    <tr>
      <th>36</th>
      <td>193482788</td>
      <td>name</td>
      <td>Westwood South</td>
      <td>neighbourhood</td>
    </tr>
    <tr>
      <th>37</th>
      <td>484782038</td>
      <td>name</td>
      <td>Goldenrod Estates</td>
      <td>neighbourhood</td>
    </tr>
    <tr>
      <th>38</th>
      <td>607795595</td>
      <td>name</td>
      <td>The Grove</td>
      <td>neighbourhood</td>
    </tr>
    <tr>
      <th>39</th>
      <td>609332847</td>
      <td>name</td>
      <td>Riverside</td>
      <td>neighbourhood</td>
    </tr>
    <tr>
      <th>40</th>
      <td>186264856</td>
      <td>name</td>
      <td>Royal Lake Estates</td>
      <td>suburb</td>
    </tr>
    <tr>
      <th>41</th>
      <td>151469708</td>
      <td>name</td>
      <td>Rosenberg</td>
      <td>town</td>
    </tr>
    <tr>
      <th>42</th>
      <td>151912936</td>
      <td>name</td>
      <td>Richmond</td>
      <td>town</td>
    </tr>
    <tr>
      <th>43</th>
      <td>151335252</td>
      <td>name</td>
      <td>Stafford</td>
      <td>village</td>
    </tr>
    <tr>
      <th>44</th>
      <td>151830706</td>
      <td>name</td>
      <td>Meadows Place</td>
      <td>village</td>
    </tr>
  </tbody>
</table>
</div>



<p>The first issue to examine is what the specific size parameters are, or should be, to designate a place as either a hamlet, town or city (increasing by population or area of sq. miles). For example, the "Town" of Richmond only claims a population of 12,033 citizens, but this does not include the Extra Territorial Jurisdictions (ETJs) attributed to Richmond. Locations with addresses listed as being in Richmond could actually cover two or three times larger than the city limits and could include a much larger population, therefore bringing into question whether it should be listed as a "town" or "city". It is unclear, however, how this could negatively affect other geographic locations as Richmond may be a circumstance unique to areas around Houston or the state of Texas.</p>
<p>The second issue would be to look at Royal Lake Estates and its designation as a "suburb". Royal Lake Estates is a residential subdivision (neighborhood) in rural Fort Bend County. I don't believe it could rightfully be classified as a "suburb" as it's only governing body is a homeowners association. This could easily be corrected in the same manner as other values have been corrected in this project, but it raises the question of whether the label "suburb" should have been applied to other places in this list as they are all part of the Houston metropolitan area. It is unclear, however, which places listed would be considered suburbs, since only Sugar Land actually borders the Houston city limits.</p>


```python

```
