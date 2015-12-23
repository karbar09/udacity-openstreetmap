#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
"""
Your task is to explore the data a bit more.
The first task is a fun one - find out how many unique users
have contributed to the map in this particular area!

The function process_map should return a set of unique user IDs ("uid")
"""

def get_user(element):
    if element.tag in ['node','way','relation']:
        return element.get('uid')
    return ""


def process_map(filename):
    users = set()
    for _, element in ET.iterparse(filename):
        u = get_user(element)
        if u != "":
            users.add(u)

    return users


def test():

    users = process_map('example.osm')
    pprint.pprint(len(users))
    assert len(users) == 6



if __name__ == "__main__":
    test()
