import logging
import discord
from discord.ext import commands

from players import get_players, is_playing
from constants import SERVER, INFO, LARGE, BOLD, ITALIC, REGULAR,COMMAND_DESC, COMMAND_USAGE, LOGO, ICON, GIT_URL

def player_embed(message):
    received = message.content.split()
    exists_params = len(received) > 1
    embed = discord.Embed(
        title='Is playing?',
        colour=discord.Colour.dark_magenta(),
        url=SERVER
    )
    embed.set_author(
        name='Hello {}!'.format(message.author.name),
        icon_url=message.author.avatar_url)
    if exists_params:
        players = get_players()
        player = received[1]
        playing = is_playing(players, player)
        if playing:
            embed.description = '😁 {} is playing'.format(player)
        else:
            embed.description = '😢 {} isn\'t playing'.format(player)
    else:
        embed.description = '😕 You must supply the name of one player'
    return embed

def players_embed():
    """
    Returns a embed message with the list of current players.
    """
    players = get_players()
    embed = discord.Embed(
        title='Player list',
        description='Current players in game',
        colour=discord.Colour.dark_magenta(),
        url=SERVER + INFO)
    embed.set_footer(
        text='https://risenfromashes.us/',
    )
    embed.set_thumbnail(
        url='https://risenfromashes.us/phpBB3/styles/digi_darkblue/theme/images/logo.png')
    middle = len(players) // 2
    pplayers1 = '{}'.format('\n'.join(['**{}**\n> score: {}\n> ping: {}\n'.
                                       format(player[0],
                                              player[1],
                                              player[2])
                                       for player in players[:middle]]))
    pplayers2 = '{}'.format('\n'.join(['**{}**\n> score: {}\n> ping: {}\n'.
                                       format(player[0],
                                              player[1],
                                              player[2])
                                       for player in players[middle:]]))
    logging.info(pplayers1)
    logging.info(pplayers2)
    embed.add_field(name='🎮', value=pplayers1, inline=False)
    embed.add_field(name='🕹', value=pplayers2, inline=False)
    return embed


def info_embed(params):
    """
    Returns a embed message with the information about the current
    map.
    """
    name_map = params['img_map'].split('/')[-1]
    url_remote_image = '{}{}{}'.format(SERVER, LARGE, name_map)
    embed = discord.Embed(
        title='Current map',
        description='Number of **{}**\nCurrent map: **{}**\n\n\n'.format(
            params['players'], params['map']),
        colour=discord.Colour.dark_magenta(),
        url=SERVER + INFO
    )

    embed.set_footer(text=SERVER)
    embed.set_image(url=url_remote_image)
    embed.set_thumbnail(
        url=LOGO)
    embed.set_author(
        name='dev by diddy',
        icon_url=ICON,
        url=GIT_URL)
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
    cmds = ['hello', 'info', 'infomap', 'players', 'player']
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
        embed.description = '**{}**: {}'.format(command, COMMAND_DESC[command])
        embed.add_field(name='Usage', value='`' + COMMAND_USAGE[command] + '`')
        embed.set_footer(text='The {} command'.format(command))
    else:
        embed.description = 'Use `-rfabot «command»` to view help on a specific command.'
        embed.add_field(name='All Commands | ' + str(len(cmds)),
                        value='`' + '`, `'.join(cmds) + '`', inline=False)
    return embed
