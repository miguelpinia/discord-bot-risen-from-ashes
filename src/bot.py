#!/usr/bin/env python3

"""Discord-bot Module"""

from os.path import expanduser
import urllib.request as request
import discord
from utils import get_token, process_data, generate_image_es, generate_image_en


TOKEN = get_token(expanduser('~/.discord_token'))
URL = "https://fallin-angels.org/servers.php?serverid=37"

TEMPLATE_ES = 'Mapa:    \t\t\t\t\t{}\nLimite Banderas:  \t{}\nBanderas\
 Rojos:\t\t{}\nBanderas Azules:\t {}\nTiempo del mapa:\t{}\nSiguiente\
 Mapa:\t\t{}'

TEMPLATE_EN = 'Map:\t\t\t\t{}\nFlags Limit:\t{}\nRed  Flags:\t\t{}\nBlue\
 Flags:\t\t{}\nMap Time:\t{}\nNext Map:\t{}'

client = discord.Client()


def next_map():
    """Information about next map."""
    file_info = request.urlopen(URL)
    data = process_data(file_info.read().decode('utf-8'))
    return 'Next Map:      {}'.format(data['next_map'])


def info_es():
    """Information about the current map in Spanish."""
    file_info = request.urlopen(URL)
    data = file_info.read().decode('utf-8')
    data = process_data(data)
    return TEMPLATE_ES.format(data['mapa'],
                              data['banderas'],
                              data['rojas'],
                              data['azules'],
                              data['tiempo'],
                              data['next_map'])


def info_en():
    """Information about the current map in english."""
    file_info = request.urlopen(URL)
    data = file_info.read().decode('utf-8')
    data = process_data(data)
    return TEMPLATE_EN.format(data['mapa'],
                              data['banderas'],
                              data['rojas'],
                              data['azules'],
                              data['tiempo'],
                              data['next_map'])


def img_es():
    """Get a image with information about the current map in spanish."""
    file_info = request.urlopen(URL)
    data = file_info.read().decode('utf-8')
    text = generate_image_es(data)
    return text


def img_en():
    """Get a image with information about the current map in spanish."""
    file_info = request.urlopen(URL)
    data = file_info.read().decode('utf-8')
    text = generate_image_en(data)
    return text


@client.event
async def on_message(message):
    """Captura todos los mensajes del canal."""
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    content = message.content.lower()

    if content == '!info_es':
        text = img_es()
        with open(text, 'rb') as archivo:
            await client.send_file(
                message.channel,
                archivo,
                content='Holis {0.author.mention}!'.format(message))
        return
    elif content == '!info_en':
        text = img_en()
        with open(text, 'rb') as archivo:
            await client.send_file(
                message.channel,
                archivo,
                content='Holis {0.author.mention}!'.format(message))
        return
    switch = {
        '!hello': 'Holis {0.author.mention}!'.format(message),
        '!map_es': 'Holis {0.author.mention}!\n{1}'.format(message, info_es()),
        '!map_en': 'Holis {0.author.mention}!\n{1}'.format(message, info_en()),
        '!next_map': 'Holis {0.author.mention}!\n{1}'.format(message, next_map())
    }
    msg = switch.get(content)
    if msg is None:
        return
    await client.send_message(message.channel, msg)


@client.event
async def on_member_join(member):
    """
    Display a message when a new member join to the server.
    """
    server = member.server
    fmt = 'Welcome {0.mention} to {1.name}!'
    await client.send_message(server, fmt.format(member, server))


@client.event
async def on_ready():
    """Imprime cuando está listo el bot."""
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
