#!/usr/bin/env python3

"""Discord-bot Module"""

import logging
from time import strftime, localtime
import urllib.request as request

import discord
from discord.ext import commands
from src.players import get_players, is_playing

from src.constants import SERVER, INFO, LARGE, BOLD, ITALIC, REGULAR,COMMAND_DESC, COMMAND_USAGE, LOGO, ICON, GIT_URL

from src.utils import get_params_from_html, image_current_map
from src.embeds import player_embed, players_embed, info_embed, help_embed


def get_token(filename):
    """Get the content of file."""
    with open(filename) as data:
        return data.readline()

TOKEN = get_token(os.path.expanduser('~/.discord_token'))

# Logging output
logging.basicConfig(
    filename='bot.log',
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p')
logging.debug('Beggining debugging')

client = commands.Bot(command_prefix='-')

def build_image_map():
    """
    Build the image with information about the current map in the
    SERVER.
    """
    server_info = SERVER + INFO
    params = get_params_from_html(server_info)
    path_image_map = image_current_map(params)
    return path_image_map


@client.event
async def on_message(message):
    """Listener for the messages sent by the discord users."""
    logging.info('Author: {}; channel: {}, message: {}'.format(
        message.author, message.channel, message.content))
    if message.author == client.user:
        return
    content = message.content.lower()
    channel = message.channel
    template = 'Hello {0.author.mention}!'.format(message)
    server_info = SERVER + INFO
    params = get_params_from_html(server_info)
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
    if content.startswith('-players'):
        psembed = players_embed()
        logging.info(psembed)
        await channel.send(embed=psembed)
        return
    if content.startswith('-player'):
        pembed = player_embed(message)
        await channel.send(embed=pembed)
        return


@client.event
async def on_ready():
    """Imprime cuando está listo el bot."""
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    activity = discord.Game('"-help" or "-rfabot" for help')
    await client.change_presence(activity=activity)

client.run(TOKEN)
