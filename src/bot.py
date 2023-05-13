#!/usr/bin/env python3

"""Discord-bot Module"""

import os
import logging
from time import strftime, localtime
import urllib.request as request

import discord
from discord import Embed
from discord.ext import commands, tasks
from discord_slash import SlashCommand, SlashContext


from constants import SERVER, INFO, LARGE, BOLD, ITALIC, REGULAR,COMMAND_DESC, COMMAND_USAGE, LOGO, ICON, GIT_URL
from players import get_players, is_playing
from utils import get_params_from_html, image_current_map
from embeds import player_embed, players_embed, info_embed, help_embed, playerlist_embed


def get_token(filename):
    """Get the content of file."""
    with open(filename) as data:
        return data.readline()

TOKEN = get_token(os.path.expanduser('~/.discord_token'))
# Channel wehre we will spam map changes.
CHANNEL = get_token(os.path.expanduser('~/.channel_token'))

# Logging output
logging.basicConfig(
    filename='bot.log',
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p')
logging.debug('Beggining debugging')
client = commands.Bot(command_prefix='-')
slash = SlashCommand(client, sync_commands=True)


@slash.slash(name='testing', description='Testing cool things')
async def pfp(ctx: SlashContext):
    embed = Embed(
        title=f'Avatar of {ctx.author.display_name}',
        color=discord.Color.teal()
    ).set_image(url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

@slash.slash(name='test')
async def test(ctx: SlashContext):
    logging.info(ctx)
    embed = Embed(title = 'Testing')
    await ctx.send(embed=embed)

@slash.slash(name='hello', description='Prints a hello message to user')
async def hello(ctx: SlashContext):
    logging.info('message: {}; author: {}, user: {}'.format(
        ctx.message, ctx.author, client.user))
    if ctx.author == client.user:
        return
    template = f'Hello {ctx.author.mention}!'
    await ctx.send(content=template)

@slash.slash(name='info', description='Display information about the current map')
async def info(ctx: SlashContext):
    server_info = SERVER + INFO
    params = get_params_from_html(server_info)
    embed = info_embed(params)
    message = f'Hey {ctx.author.mention}! Here\'s the information requested 👩‍🕵'
    await ctx.send(content=message, embed=embed)

@slash.slash(name='map', description='Get an image with information about the current map')
async def map(ctx: SlashContext):
    file_map = build_image_map()
    message = f'Hey {ctx.author.mention}! Here\'s your image 😉⚡'
    with open(file_map, 'rb') as document:
        await ctx.send(content=message,
                       file=discord.File(document.name,
                                         document.name))

@slash.slash(name='list', description='Get the list of players nicely formatted')
async def list(ctx: SlashContext):
    embed, img = playerlist_embed(ctx)
    message = f'{ctx.author.mention}, here\'s the list of players'
    await ctx.send(content=message, embed=embed, file=img)


@slash.slash(name='players', description='Get the list of players')
async def players(ctx: SlashContext):
    embed = players_embed()
    message = f'{ctx.author.mention}, here\'s the list of players'
    await ctx.send(content=message, embed=embed)

def build_image_map():
    """
    Build the image with information about the current map in the
    SERVER.
    """
    server_info = SERVER + INFO
    params = get_params_from_html(server_info)
    path_image_map = image_current_map(params)
    return path_image_map

class LoopInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.current = 'default'
        self.loop_information.start()

    def cog_unload(self):
        self.loop_information.cancel()

    @tasks.loop(minutes=1)
    async def loop_information(self):
        channel = self.bot.get_channel(int(CHANNEL))
        server_info = SERVER + INFO
        params = get_params_from_html(server_info)
        if any(params):
            logging.info('Current map: {}, map params: {}'.format(self.current,
                                                                  params['map']))
            if self.current != params['map']:
                self.current = params['map']
                logging.info('Channel {}, params: {}'.format(channel, params))
                embed = info_embed(params)
                await channel.send(content='@here The map has changed', embed=embed)

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
        logging.info('Channel: {}, channel_ID: {}, '.format(channel, channel.id))
        channel2 = client.get_channel(channel.id)
        logging.info('Testing channel {}'.format(channel2))
        await channel.send(embed=iembed)
        return
    if content.startswith('-rfabot') or content.startswith('-help'):
        hembed = help_embed(message)
        await channel.send(embed=hembed)
        return
    if content.startswith('-playerlist'):
        nembed, img = playerlist_embed(message)
        await channel.send(embed=nembed, file=img)
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
    client.add_cog(LoopInfo(client))


client.run(TOKEN)
