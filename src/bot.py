#!/usr/bin/env python3

"""Discord-bot Module"""

import os
import urllib.request as request
from re import compile as comp, sub
from pathlib import Path
from time import strftime, localtime
from PIL import Image, ImageDraw, ImageFont

import discord
from discord.ext import commands


def get_token(filename):
    """Get the content of file."""
    with open(filename) as data:
        return data.readline()


TOKEN = get_token(os.path.expanduser('~/.discord_token'))
SERVER = 'https://risenfromashes.us'
INFO = '/info/serverinfo.php'
URL = SERVER + INFO
LARGE = '/rfamaps/content/bin/images/large/'
BOLD = os.path.abspath('deps/Input-Bold_(InputMono-Bold).ttf')
ITALIC = os.path.abspath('deps/Input-BoldItalic_(InputMono-BoldItalic).ttf')
REGULAR = os.path.abspath('deps/Input-Regular_(InputMono-Regular).ttf')
FNT = ImageFont.truetype(BOLD, 24)
FNT2 = ImageFont.truetype(ITALIC, 16)
FNT3 = ImageFont.truetype(REGULAR, 18)

client = commands.Bot(command_prefix='-')

cmd_desc = {
    'hello': 'Prints a hello message',
    'info': 'Display a message with the information about the current map in the server',
    'infomap': 'Display a image with the information about the current map in the server'
}

cmd_usages = {
    'hello': '-hello',
    'info': '-info',
    'infomap': '-infomap'
}


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


def html_process(server_url):
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
    text.text((10, 320), 'Map', font=FNT, fill=(255, 255, 255))
    text.text((220, 328), params['map'], font=FNT2, fill=(255, 255, 255))
    text.text((10, 380), params['players'], font=FNT3, fill=(0, 0, 0))
    text.text((220, 383), '', font=FNT2, fill=(0, 0, 0))
    text.text((10, 410), 'Next Map', font=FNT3, fill=(255, 0, 0))
    text.text((180, 413), params['nextmap1'], font=FNT2, fill=(255, 0, 0))
    text.text((10, 435), 'Next Map 2', font=FNT3, fill=(0, 0, 255))
    text.text((180, 438), params['nextmap2'], font=FNT2, fill=(0, 0, 255))
    text.text((10, 460), 'Next Map 3', font=FNT3, fill=(255, 0, 255))
    text.text((180, 463), params['nextmap3'], font=FNT2, fill=(255, 0, 255))
    text.text((10, 485), 'Capture limit', font=FNT3, fill=(0, 0, 0))
    text.text((180, 488), params['capturelimit'], font=FNT2, fill=(0, 0, 0))
    path_new_img = '/tmp/{}_{}.jpg'.format(
        strftime('%Y-%m-%d-%H:%M:%S', localtime()), 'en')
    base.save(path_new_img)
    return path_new_img


def build_image_map():
    """
    Build the image with information about the current map in the
    SERVER.
    """
    server_info = SERVER + INFO
    params = html_process(server_info)
    path_image_map = image_current_map(params)
    return path_image_map


def info_embed(params):
    """
    Returns a embed message with the information about the current
    map.
    """
    name_map = params['img_map'].split('/')[-1]
    url_remote_image = '{}{}{}'.format(SERVER, LARGE, name_map)
    embed = discord.Embed(
        title='Current map',
        description='Number of **' +
        params['players'] + '**\nCurrent map: **' + params['map'] + '**\n\n\n',
        colour=discord.Colour.dark_magenta(),
        url=SERVER + INFO
    )

    embed.set_footer(
        text='https://risenfromashes.us/',
    )
    embed.set_image(url=url_remote_image)
    embed.set_thumbnail(
        url='https://risenfromashes.us/phpBB3/styles/digi_darkblue/theme/images/logo.png')
    embed.set_author(
        name='dev by diddy',
        icon_url='https://cdn.discordapp.com/avatars/614999407233859622/2a613a71917c27bd89f8a06b145b95ed.png?size=128',
        url='https://github.com/miguelpinia/discord-bot-risen-from-ashes')
    embed.add_field(
        name='😴 Capture Limit',
        value=params['capturelimit'],
        inline=False)
    embed.add_field(
        name='😱 Next Map 1',
        value=params['nextmap1'],
        inline=False)
    embed.add_field(
        name='🙄 Next Map 2',
        value=params['nextmap2'],
        inline=False)
    embed.add_field(
        name='🥰 Next Map 3',
        value=params['nextmap3'],
        inline=False)
    return embed


def help_embed(message):
    """
    Returns a embed message with helpful information about the
    commands and the help system.
    """
    cmds = ['hello', 'info', 'infomap']
    content = message.content.lower()
    received = content.split()
    exists_command = len(received) > 1
    embed = discord.Embed(
        title='Help',
        colour=discord.Colour.dark_magenta(),
        url=SERVER
    )
    embed.set_author(
        name='Hello {}!'.format(message.author.name),
        icon_url=message.author.avatar_url)
    if exists_command:
        command = received[1]
        if command not in cmds:
            embed.description = 'The command **{}** does not exist!'.format(
                command)
            return embed
        embed.description = '**{}**: {}'.format(command, cmd_desc[command])
        embed.add_field(name='Usage', value='`' + cmd_usages[command] + '`')
        embed.set_footer(text='The {} command'.format(command))
    else:
        embed.description = 'Use `-rfabot «command»` to view help on a specific command.'
        embed.add_field(name='All Commands | ' + str(len(cmds)),
                        value='`' + '`, `'.join(cmds) + '`', inline=False)
    return embed


@client.event
async def on_message(message):
    """Listener for the messages sent by the discord users."""
    print('Author: {}; channel: {}, message: {}'.format(
        message.author, message.channel, message.content))
    if message.author == client.user:
        return
    content = message.content.lower()
    channel = message.channel
    template = 'Hello {0.author.mention}!'.format(message)
    server_info = SERVER + INFO
    params = html_process(server_info)
    if content.startswith('-hello'):
        await message.channel.send(template)
        return
    if content.startswith('-infomap'):
        file_map = build_image_map()
        with open(file_map, 'rb') as document:
            await channel.send(file=discord.File(document.name,
                                                 document.name))
        return
    if content.startswith('-info'):
        iembed = info_embed(params)
        await channel.send(embed=iembed)
        return
    if content.startswith('-rfabot') or content.startswith('-help'):
        hembed = help_embed(message)
        await channel.send(embed=hembed)
        return


@client.event
async def on_ready():
    """Imprime cuando está listo el bot."""
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    activity = discord.Game('"-rfabot" or "-help" for help')
    await client.change_presence(activity=activity)

client.run(TOKEN)
