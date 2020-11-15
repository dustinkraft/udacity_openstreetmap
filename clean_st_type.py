#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

OSMFILE = "sugarroserich.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

# Ignore street names ending in expected words
expected = ["Street", "Avenue", "Boulevard", "Drive", "Lane", "Road", "Parkway", "Freeway", "Way", "Court", "Crossing", "Circle", "Walk"]

# Map abbreviations to full words
mapping = { "St": "Street",
            "Rd": "Road",
            "Cir": "Circle",
            "Blvd": "Boulevard",
            "Fwy": "Freeway",
            "pkwy": "Parkway"
            }

def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

# Function used by data.py to clean street type values
def update_name(name, mapping):
    m = street_type_re.search(name)
    if m:
        street_type = m.group()
        if street_type not in expected and street_type in mapping:
            name = re.sub(street_type_re, mapping[street_type], name)

    return name