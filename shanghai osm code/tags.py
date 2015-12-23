#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
"""
Adapted to project 6
"""


lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')


def key_type(element, keys):
    if element.tag == "tag":
        # YOUR CODE HERE
        if lower.match(element.get('k')):
            keys['lower'] += 1
        elif lower_colon.match(element.get('k')):
            keys['lower_colon'] += 1
        elif problemchars.match(element.get('k')):
            keys['problemchars'] += 1
        else:
            keys['other'] += 1
        
        
    return keys



def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    return keys



def test():
    keys = process_map('shanghai_china.osm')
    pprint.pprint(keys)

if __name__ == "__main__":
    test()
