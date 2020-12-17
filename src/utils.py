import os
from re import compile as comp, sub
import urllib.request as request
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from time import strftime, localtime

from constants import BOLD, ITALIC, REGULAR, SERVER, LARGE

FONT1 = ImageFont.truetype(os.path.abspath(BOLD), 24)
FONT2 = ImageFont.truetype(os.path.abspath(ITALIC), 16)
FONT3 = ImageFont.truetype(os.path.abspath(REGULAR), 18)

def get_html_content(server_url):
    """Retrieve the html content from the `server_url` specified."""
    html = request.urlopen(server_url)
    html = html.read().decode('utf-8')
    return html

def string_filter(query, content):
    """
    Returns all rows that contains the string `string` in the html
    contente.
    """
    rows_html = content.split('\n')
    return list(filter(lambda row: query in row[1], enumerate(rows_html)))

def clean_html(raw_html):
    """Remove tags from `raw_html`"""
    return sub(comp('<.*?>'), '', raw_html).strip()

def __get_img_loc(idx, rows):
    location = rows[idx] + rows[idx + 1]
    location = location[location.find('src=') + 5:]
    location = location[:location.find('jpg') + 3]
    return location


def get_params_from_html(server_url):
    """
    Retrieves and process the HTML from the url `server_url`. Returns a
    dictionary with the following keys-values:

    - map
    - image_map
    - nextmap1
    - img_nextmap1
    - nextmap2
    - img_nextmap2
    - nextmap3
    - img_nextmap3
    - capturelimit
    - players
    """
    html = get_html_content(server_url)
    html_rows = html.split('\n')
    indexes = {'idx_mapname': string_filter('mapname', html)[0][0],
               'idx_nextmap1': string_filter('nextmap1', html)[0][0],
               'idx_nextmap2': string_filter('nextmap2', html)[0][0],
               'idx_nextmap3': string_filter('nextmap3', html)[0][0],
               'idx_capturelimit': string_filter('capturelimit', html)[0][0],
               'idx_players': string_filter('Players', html)[0][0]}
    values = {'map': clean_html(html_rows[indexes['idx_mapname'] + 1]),
              'img_map': __get_img_loc(indexes['idx_mapname'] + 2, html_rows),
              'nextmap1': clean_html(html_rows[indexes['idx_nextmap1'] + 1]),
              'img_nextmap1': __get_img_loc(indexes['idx_nextmap1'] + 2, html_rows),
              'nextmap2': clean_html(html_rows[indexes['idx_nextmap2'] + 1]),
              'img_nextmap2': __get_img_loc(indexes['idx_nextmap2'] + 2, html_rows),
              'nextmap3': clean_html(html_rows[indexes['idx_nextmap3'] + 1]),
              'img_nextmap3': __get_img_loc(indexes['idx_nextmap3'] + 2, html_rows),
              'capturelimit': clean_html(html_rows[indexes['idx_capturelimit'] + 1]),
              'players': clean_html(html_rows[indexes['idx_players']]), }
    return values


def get_image_map(uri):
    """Get the basic map image from the `SERVER`/`uri`"""
    name_map = uri.split('/')[-1]
    url_remote_image = '{}{}'.format(SERVER, uri)
    local_image = '/tmp/{}'.format(name_map)
    path_image = Path(local_image)
    if not path_image.exists():
        request.urlretrieve(url_remote_image, local_image)
    return local_image

def get_largeimage_map(uri):
    """Get a larger version of a map image from `SERVER`/`LARGE`/`name_map`"""
    name_map = uri.split('/')[-1]
    url_remote_image = '{}{}{}'.format(SERVER, LARGE, name_map)
    local_image = '/tmp/{}'.format(name_map)
    path_image = Path(local_image)
    if not path_image.exists():
        request.urlretrieve(url_remote_image, local_image)
    return local_image


def image_current_map(params):
    """
    Build the image with information about the current map with
    parameters given.
    """
    image_map = get_largeimage_map(params['img_map'])
    image = Image.open(image_map)
    resized = image.resize((400, 300))
    base = Image.new('RGB', (400, 600), color=(201, 201, 255))
    background = Image.new('RGB', (400, 60), color=(73, 109, 137))
    base.paste(resized)
    base.paste(background, (0, 300, 400, 360))
    text = ImageDraw.Draw(base)
    text.text((10, 320), 'Map', font=FONT1, fill=(255, 255, 255))
    text.text((220, 328), params['map'], font=FONT2, fill=(255, 255, 255))
    text.text((10, 380), params['players'], font=FONT3, fill=(0, 0, 0))
    text.text((220, 383), '', font=FONT2, fill=(0, 0, 0))
    text.text((10, 410), 'Next Map', font=FONT3, fill=(255, 0, 0))
    text.text((180, 413), params['nextmap1'], font=FONT2, fill=(255, 0, 0))
    text.text((10, 435), 'Next Map 2', font=FONT3, fill=(0, 0, 255))
    text.text((180, 438), params['nextmap2'], font=FONT2, fill=(0, 0, 255))
    text.text((10, 460), 'Next Map 3', font=FONT3, fill=(255, 0, 255))
    text.text((180, 463), params['nextmap3'], font=FONT2, fill=(255, 0, 255))
    text.text((10, 485), 'Capture limit', font=FONT3, fill=(0, 0, 0))
    text.text((180, 488), params['capturelimit'], font=FONT2, fill=(0, 0, 0))
    path_new_img = '/tmp/{}_{}.jpg'.format(
        strftime('%Y-%m-%d-%H:%M:%S', localtime()), 'en')
    base.save(path_new_img)
    return path_new_img
