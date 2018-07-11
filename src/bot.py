#!/usr/bin/env python3

"""Discord-bot Module"""

from os.path import expanduser
import urllib.request as request
import discord
from utils import get_token, process_data


TOKEN = get_token(expanduser('~/.discord_token'))
URL = "https://fallin-angels.org/servers.php?serverid=37"
client = discord.Client()


def mapa_esp(datos):
    return 'Mapa:    \t\t\t\t\t{}\nLimite Banderas:  \t{}\nBanderas Rojos:\t\t{}\nBanderas \
Azules:\t {}\nTiempo del mapa:\t{}\nSiguiente Mapa:\t\t{}'.format(datos['mapa'],
                                                                  datos['banderas'],
                                                                  datos['rojas'],
                                                                  datos['azules'],
                                                                  datos['tiempo'],
                                                                  datos['next_map'])

def map_eng(data):
    return 'Map:\t\t\t\t{}\nFlags Limit:\t{}\nRed  Flags:\t\t{}\nBlue Flags:\t\t{}\n\
Map Time:\t{}\nNext Map:\t{}'.format(data['mapa'],
                                     data['banderas'],
                                     data['rojas'],
                                     data['azules'],
                                     data['tiempo'],
                                     data['next_map'])

def next_map():
    file_info = request.urlopen(URL)
    data = process_data(file_info.read().decode('utf-8'))
    return 'Next Map:      {}'.format(data['next_map'])

def info_es():
    file_info = request.urlopen(URL)
    data = file_info.read().decode('utf-8')
    return mapa_esp(process_data(data))

def info_en():
    file_info = request.urlopen(URL)
    data = file_info.read().decode('utf-8')
    return map_eng(process_data(data))


@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    content = message.content.lower()
    switch = {
        '!hello':   'Holis {0.author.mention}!'.format(message),
        '!map_es':  'Holis {0.author.mention}!\n{1}'.format(message, info_es()),
        '!map_en':  'Holis {0.author.mention}!\n{1}'.format(message, info_en()),
        '!next_map': 'Holis {0.author.mention}!\n{1}'.format(message, next_map())
    }
    msg = switch.get(content)
    if msg is None:
        return
    await client.send_message(message.channel, msg)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
