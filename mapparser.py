#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Adapted to project 6
"""
import xml.etree.cElementTree as ET
import pprint

def count_tags(filename):
    # YOUR CODE HERE
    tree = ET.parse(filename)
    root = tree.getroot()
    tags = {}
    for r in root.iter():
        if r.tag not in tags:
            tags[r.tag] = 1
        else:
            tags[r.tag] += 1
    return tags


def test():

    tags = count_tags('shanghai_china.osm')
    pprint.pprint(tags)

if __name__ == "__main__":
    test()
