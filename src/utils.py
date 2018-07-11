#!/usr/bin/env python3

"""Utils module."""

from re import compile as comp, sub


def get_token(filename):
    """Get the content of file."""
    with open(filename) as data:
        return data.readline()


def clean_html(raw_html):
    """Remove tags from raw_html"""
    return sub(comp('<.*?>'), '', raw_html)


def process_data(data):
    """
    Returns a dictionary with keys associated with map='Mapa',
    flag_limit='Banderas', flag reds='rojas', flag blues='azules',
    current_time='tiempo' and next_map='next_map'
    """
    data = data.split('\n')
    idx = list(filter(lambda v: '<b>Map:</b>' in v[1],
                      [(i, d) for i, d in enumerate(data)]))[0][0]
    dicc = {'mapa': clean_html(data[idx + 3]).strip(),
            'banderas': clean_html(data[idx + 13]).strip(),
            'rojas': clean_html(data[idx + 16]).strip(),
            'azules': clean_html(data[idx + 19]).strip(),
            'tiempo': clean_html(data[idx + 25]).strip(),
            'next_map': clean_html(data[idx + 52]).strip()}
    return dicc
