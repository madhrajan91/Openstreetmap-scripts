Openstreetmap-scripts
=====================
Scripts that parse and clean OpenStreetMap data: http://www.openstreetmap.org/ as part of the course data wrangling with MongoDB

db_script.py : a script that inserts nodes and ways from osm files which are in xml to a mongodb collection

users.py : a script that queries the number of unique users who have contributed to this dataset.

tags.py : a script that parses the tag 'tag' and see if there are a few discrepencies in the key attributes. example: <tag k='addr:street' v='east university dr'/> where k should actually be 'address:value'



