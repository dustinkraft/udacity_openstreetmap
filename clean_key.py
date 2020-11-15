#!/usr/bin/env python
# -*- coding: utf-8 -*-

mapping = { "county": "county_name" }

# Make key string lower case and match to mapping dict
def update_key(name, mapping):
    key = name.lower()
    if key in mapping:
        name = mapping[key]
    else:
        name = key
    return name
