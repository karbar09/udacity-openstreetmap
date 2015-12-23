#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re

#Adapted to Project 6

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
    users = process_map('shanghai_china.osm')
    pprint.pprint(len(users))

if __name__ == "__main__":
    test()
