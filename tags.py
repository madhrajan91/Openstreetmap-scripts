#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import pprint
import re
"""
Your task is to explore the data a bit more.
Before you process the data and add it into MongoDB, you should
check the "k" value for each "<tag>" and see if they can be valid keys in MongoDB,
as well as see if there are any other potential problems.

We have provided you with 3 regular expressions to check for certain patterns
in the tags. As we saw in the quiz earlier, we would like to change the data model
and expand the "addr:street" type of keys to a dictionary like this:
{"address": {"street": "Some value"}}
So, we have to see if we have such tags, and if we have any tags with problematic characters.
Please complete the function 'key_type'.
"""


lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')


def key_type(element, keys):
    #parse the tags and see if the key of each tag matches the 3 regular expressions, if it does then increment the counter assigned for that regex and store it in a dictionary.
    if element.tag == "tag":
        # YOUR CODE HERE
        k = element.attrib['k']
        l_res = re.match(lower, k)
        l_colon_res = re.match(lower_colon, k)
        prb_chars_res = re.match(problemchars, k)
        if l_res != None:
            keys['lower']+=1 #increment lower case match
        elif l_colon_res != None:
            keys['lower_colon']+=1 #increment lower case colon match
        elif prb_chars_res != None:
            print k
            keys['problemchars']+=1 #increment if there is a match for problematic characters
        else:
            keys['other']+=1 #increment if the above three fails.
        pass
    
    return keys



def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    return keys



def test():
    # You can use another testfile 'map.osm' to look at your solution
    # Note that the assertions will be incorrect then.
    keys = process_map('example.osm')
    pprint.pprint(keys)
    
    #assert keys == {'lower': 5, 'lower_colon': 0, 'other': 2, 'problemchars': 0}


if __name__ == "__main__":
    test()