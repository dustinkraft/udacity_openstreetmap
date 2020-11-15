#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

st_mapping = { 
    '1092': "Farm to Market 1092",
    '1464': "Farm to Market 1464",
    '1640': "Farm to Market 1640",
    '200': "East US Highway 90 Alt",
    '285': "Southwest Freeway",
    '300': "Southwest Freeway",
    '359': "Farm to Market 359",
    '36': "TX Highway 36",
    '59': "Southwest Freeway",
    '6': "TX Highway 6",
    '77478': "TX Highway 6",
    '90': "US Highway 90", 
    '90A': "US Highway 90 Alt",
    '90a': "US Highway 90 Alt",
    'Alt': "East US Highway 90 Alt", 
    'Fm1640': "Farm to Market 1640",
    'Fm359': "Farm to Market 359",
    'T2008': "Southwest Freeway",
    'road': "Farm to Market 762"
    }

# Determine if element is a street
def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

# if element is a street and contains a key from the dict, replace name with value
def update_st_name(name, st_mapping):
    m = street_type_re.search(name)
    if m:
        street_type = m.group()
        if street_type in st_mapping:
            name = st_mapping[street_type]

    return name