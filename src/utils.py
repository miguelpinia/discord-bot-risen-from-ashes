#!/usr/bin/env python3

"""Utils module."""

from __future__ import print_function
from re import compile as comp, sub
import urllib.request as request
from time import gmtime, strftime
from pathlib import Path
from os.path import expanduser
from PIL import Image, ImageDraw, ImageFont


SERVER = "https://fallin-angels.org"
FNT = ImageFont.truetype(expanduser(
    '~/config/cfg/fonts/Input-Bold_(InputMono-Bold).ttf'), 24)
FNT2 = ImageFont.truetype(expanduser(
    '~/config/cfg/fonts/Input-BoldItalic_(InputMono-BoldItalic).ttf'), 16)
FNT3 = ImageFont.truetype(expanduser(
    '~/config/cfg/fonts/Input-Bold_(InputMono-Bold).ttf'), 18)


def get_token(filename):
    """Get the content of file."""
    with open(filename) as data:
        return data.readline()


def clean_html(raw_html):
    """Remove tags from raw_html"""
    return sub(comp('<.*?>'), '', raw_html)


def filtra_cadena(cadena, data):
    """
    Filtra todas las cadenas que aparean con CADENA dentro de DATA.
    """
    datos = data.split('\n')
    return list(filter(lambda v: cadena in v[1],
                       [(i, d) for i, d in enumerate(datos)]))


def process_data(data):
    """
    Returns a dictionary with keys associated with map='Mapa',
    flag_limit='Banderas', flag reds='rojas', flag blues='azules',
    current_time='tiempo' and next_map='next_map'
    """
    datos = data.split('\n')
    idx = filtra_cadena('<b>Map:</b>', data)[0][0]
    dicc = {'mapa': clean_html(datos[idx + 3]).strip(),
            'banderas': clean_html(datos[idx + 13]).strip(),
            'rojas': clean_html(datos[idx + 16]).strip(),
            'azules': clean_html(datos[idx + 19]).strip(),
            'tiempo': clean_html(datos[idx + 25]).strip(),
            'next_map': clean_html(datos[idx + 52]).strip()}
    return dicc


def __get_img_loc(data):
    cadena = filtra_cadena('img', data)[1][1]
    img = [v for v in cadena.split('"') if 'urtmaps' in v][0]
    name_map = img.split('/')[-1]
    resimg = '{}{}'.format(SERVER, img)
    local_img = '/tmp/{}'.format(name_map)
    my_img = Path(local_img)
    if not my_img.exists():
        request.urlretrieve(resimg, local_img)
    return local_img


def __image_base(data, labels, lan='es'):
    local_img = __get_img_loc(data)
    img = Image.open(local_img)
    box = (0, 0, 600, 450)
    resized = img.crop(box).resize((400, 300))
    res = Image.new('RGB', (400, 600), color=(201, 201, 255))
    color = Image.new('RGB', (400, 60), color=(73, 109, 137))
    res.paste(resized)
    res.paste(color, (0, 300, 400, 360))
    text = ImageDraw.Draw(res)
    datos = process_data(data)
    text.text((10, 320), labels['map'], font=FNT, fill=(255, 255, 255))
    text.text((220, 328), datos['mapa'], font=FNT2, fill=(255, 255, 255))
    text.text((10, 380), labels['limit'], font=FNT3, fill=(0, 0, 0))
    text.text((220, 383), datos['banderas'], font=FNT2, fill=(0, 0, 0))
    text.text((10, 410), labels['reds'], font=FNT3, fill=(255, 0, 0))
    text.text((220, 413), datos['rojas'], font=FNT2, fill=(255, 0, 0))
    text.text((10, 435), labels['blues'], font=FNT3, fill=(0, 0, 255))
    text.text((220, 438), datos['azules'], font=FNT2, fill=(0, 0, 255))
    text.text((10, 460), labels['time'], font=FNT3, fill=(0, 0, 0))
    text.text((220, 463), datos['tiempo'], font=FNT2, fill=(0, 0, 0))
    text.text((10, 485), labels['next'], font=FNT3, fill=(0, 0, 0))
    text.text((220, 488), datos['next_map'], font=FNT2, fill=(0, 0, 0))
    t_img = '/tmp/{}_{}.jpg'.format(strftime("%Y-%m-%d-%H:%M:%S", gmtime()),
                                    lan)
    res.save(t_img)
    return t_img


def generate_image_es(data):
    """Genera una nueva imagen."""
    labels = {'map': 'Mapa actual:',
              'limit': 'Límite banderas:',
              'reds': 'Banderas rojas:',
              'blues': 'Banderas azules:',
              'time': 'Tiempo del mapa:',
              'next': 'Siguiente mapa:'}
    return __image_base(data, labels)


def generate_image_en(data):
    """Create a new image in english"""
    labels = {'map': 'Current Map:',
              'limit': 'Flags Limit:',
              'reds': 'Red Flags:',
              'blues': 'Blue Flags:',
              'time': 'Map Time:',
              'next': 'Next map:'}
    return __image_base(data, labels, 'en')
