#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import pprint
import re
"""
Your task is to explore the data a bit more.
The first task is a fun one - find out how many unique users
have contributed to the map in this particular area!

The function process_map should return a set of unique user IDs ("uid")
"""

def get_user(element):
    return


def process_map(filename):
    users = set()
    #iterate through the file and if the user is not in the set, add the user to the set.
    for _, element in ET.iterparse(filename):
        if 'user' in element.attrib.keys():
            if element.attrib['user'] not in users:
                users.add(element.attrib['user'])
        pass

    return users


def test():

    users = process_map('example.osm')
    pprint.pprint(users)
    #assert len(users) == 6



if __name__ == "__main__":
    test()