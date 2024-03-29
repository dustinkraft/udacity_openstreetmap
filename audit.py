#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "c:/Users/Dustin/Desktop/openstreetmapproject/sugarroserich.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

# Ignore street names ending in expected words
expected = ["Street", "Avenue", "Boulevard", "Drive", "Lane", "Road", "Parkway", "Freeway", "Way", "Court", "Crossing", "Circle", "Walk"]

def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

def audit(osmfile):
    osm_file = open(osmfile, "r",  encoding="utf-8")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    osm_file.close()
    return street_types

def test():
    st_types = audit(OSMFILE)
    pprint.pprint(dict(st_types))


if __name__ == '__main__':
    test()