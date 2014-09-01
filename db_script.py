#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import pprint
import re
import codecs
import json
from pymongo import MongoClient

# cleans and inserts the records of nodes and ways into a mongodb collection
# The name of the database is examples and the data is inserted into the collection called phoenix.

"""
Output:

{
"id": "2406124091",
"type: "node",
"visible":"true",
"created": {
          "version":"2",
          "changeset":"17206049",
          "timestamp":"2013-08-03T16:43:42Z",
          "user":"linuxUser16",
          "uid":"1219059"
        },
"pos": [41.9757030, -87.6921867],
"address": {
          "housenumber": "5157",
          "postcode": "60625",
          "street": "North Lincoln Ave"
        },
"amenity": "restaurant",
"cuisine": "mexican",
"name": "La Cabana De Don Luis",
"phone": "1 (773)-271-5176"
}


In particular the following things has been done:
-  process only 2 types of top level tags: "node" and "way"
- all attributes of "node" and "way" should be turned into regular key/value pairs, except:
    - attributes in the CREATED array should be added under a key "created"
    - attributes for latitude and longitude should be added to a "pos" array,
      for use in geospacial indexing. Make sure the values inside "pos" array are floats
      and not strings. 
- if second level tag "k" value contains problematic characters, it should be ignored
- if second level tag "k" value starts with "addr:", it should be added to a dictionary "address"
- if second level tag "k" value does not start with "addr:", but contains ":", you can process it
  same as any other tag.
- if there is a second ":" that separates the type/direction of a street,
  the tag should be ignored, for example:

<tag k="addr:housenumber" v="5158"/>
<tag k="addr:street" v="North Lincoln Avenue"/>
<tag k="addr:street:name" v="Lincoln"/>
<tag k="addr:street:prefix" v="North"/>
<tag k="addr:street:type" v="Avenue"/>
<tag k="amenity" v="pharmacy"/>

  should be turned into:

{...
"address": {
    "housenumber": 5158,
    "street": "North Lincoln Avenue"
}
"amenity": "pharmacy",
...
}

- for "way" specifically:

  <nd ref="305896090"/>
  <nd ref="1719825889"/>

should be turned into
"node_ref": ["305896090", "1719825889"]
"""


lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]


def shape_element(element):
    node = {}
    if element.tag != 'node' and element.tag != 'way':
        return None 
    if element.tag == "node" or element.tag == "way" :
        # YOUR CODE HERE
        node['id'] = element.attrib['id']
        
        #node['type'] = element.attrib['type']
        created = {}
        #assign created using the attirbutes
        created['version'] = element.attrib['version']
        created['changeset'] = element.attrib['changeset']
        created['timestamp'] = element.attrib['timestamp']
        created['user'] = element.attrib['user']
        created['uid'] = element.attrib['uid']
        #print element.attrib['lat'], ' ', element.attrib['lon']
        if 'visible' in element.attrib.keys():
            node['visible'] = element.attrib['visible']
            
        # check if type == node or type == way to assign types
        if element.tag == 'node':
            node['type']='node'
            
            lat = float(element.attrib['lat'])
            lon = float(element.attrib['lon'])
            pos=[lat, lon]
            node['pos'] = pos
        else:
            node['type'] = 'way'
            ndref = []
            for nd in element.iter('nd'):
               ndref.append(nd.attrib['ref'])
            node['node_refs'] = ndref
                
       
        
        
        node['created'] = created
        address={}
        #Iterate through tags
        for child in element.iter('tag'):
            if re.match(problemchars, child.attrib['k']) == None:
                if 'null' in child.attrib['v']: #ignore the key if the value is null
                    continue
                if '.' in child.attrib['k']: #replace . in places like address.city to address:city
                    child.attrib['k'] = child.attrib['k'].replace('.', ':')
                if 'addr' in child.attrib['k']: #replace addr example addr:city to address:city
                    child.attrib['k'] = child.attrib['k'].replace('addr', 'address')
                if ':' in child.attrib['k']:
                    data = child.attrib['k'].split(':')
                    if len(data) == 2:
                        if data[0]=='addr' or data[0]=='address':
                            address[data[1]] = child.attrib['v']
                            node['address'] = address
                        else:
                            node[child.attrib['k']]=child.attrib['v']
                else:
                    node[child.attrib['k']] = child.attrib['v']
                     
         
        
        
        return node
    else:
        return None


def process_map(file_in, pretty = False):
    # You do not need to change this
    data = []
    # Initialize mongodb client
    client = MongoClient("mongodb://localhost:27017") #make the connection to the mongdb database
    db = client.examples    #initializae the database that you want
    for _, element in ET.iterparse(file_in):
        el = shape_element(element)
        if el:
            data.append(el)
            #Insert into the collection
            db.phoenix.insert(el) #insert it into your connection. I've used phoenix osm data

    return data

def test():

data = process_map('example.osm', True) #Input osm file name
    pprint.pprint(data[0])
    """
    assert data[0] == {
                        "id": "261114295", 
                        "visible": "true", 
                        "type": "node", 
                        "pos": [
                          41.9730791, 
                          -87.6866303
                        ], 
                        "created": {
                          "changeset": "11129782", 
                          "user": "bbmiller", 
                          "version": "7", 
                          "uid": "451048", 
                          "timestamp": "2012-03-28T18:31:23Z"
                        }
                      }
    assert data[-1]["address"] == {
                                    "street": "West Lexington St.", 
                                    "housenumber": "1412"
                                      }
    assert data[-1]["node_refs"] == [ "2199822281", "2199822390",  "2199822392", "2199822369", 
                                    "2199822370", "2199822284", "2199822281"]
    """

if __name__ == "__main__":
    test()