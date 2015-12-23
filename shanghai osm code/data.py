#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json
from audit import update_name
"""
Adapted to project 6
"""


lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]
improper_address = ["S308","3"]
def shape_element(element):
    node = {}
    if element.tag == "node" or element.tag == "way" :
        # YOUR CODE HERE
        lat_lon_array = [0,0]
        has_pos = False
        created_dict = {}
        node['type'] = element.tag
        for key,value in element.attrib.iteritems():
            if key in CREATED:
                created_dict[key] = value
            elif key in ['lat','lon']:
                has_pos = True
                if key == 'lat':
                    lat_lon_array[0] = float(value)
                else:
                    lat_lon_array[1] = float(value)
            else:
                node[key] = value
        address = {}
        has_address = False
        for tag in element.iter('tag'):
            if problemchars.search(tag.get('k')) is not None or len(tag.get('k').split(":"))>2:
                continue
            elif 'addr:' in tag.get('k'):
                has_address = True
                addr_list = tag.get('k').split(":")
                if addr_list[1] == 'street':
                    #if address is an "improper_address", then skip this tag.
                    if tag.get('v') not in improper_address:
                        address[addr_list[1]] = update_name(tag.get('v'))         
                    else:
                        print tag.get('v')
                        continue           
                else:
                    address[addr_list[1]] = tag.get('v')
                    
            else:
                node[tag.get('k')] = tag.get('v')
        
        node_refs = []
        has_node_refs = False
        for tag in element.iter('nd'):
            has_node_refs = True
            node_refs.append(tag.get('ref'))
        if has_node_refs:
            node['node_refs'] = node_refs
        node['created'] = created_dict
        if has_pos:
            node['pos'] = lat_lon_array
        if has_address:
            node['address'] = address
        return node
    else:
        return None


def process_map(file_in, pretty = False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data

def test():
    data = process_map('shanghai_china.osm', False)
    # print the first 10 records
    pprint.pprint(data[:10])


if __name__ == "__main__":
    test()
