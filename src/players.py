"""
Module: Players

Get all information related to players.
"""

from re import compile as comp, sub
import urllib.request as request

from bs4 import BeautifulSoup


def clean_html(raw_html):
    """Remove tags from `raw_html`"""
    return sub(comp('<.*?>'), '', raw_html).strip()


def chunks(lst, size):
    """
    Build a (generator) list of chucks of size 'size' from the list
    'list'. Example:

    >> p = ['spectri', '8', '150', '13', 'BAT', '5', '148', '1', 'Beny', '5', '148', '3']
    >>> print(p, list(chunks(p, 4)))
    [['spectri', '8', '150', '13'], ['BAT', '5', '148', '1'], ['Beny', '5', '148', '3']]
    """
    for i in range(0, len(lst), size):
        yield lst[i: i + size]


def get_players():
    """
    Get the list of players in chunks of list. Every sublist
    contains the name, score, ping and order.
    """
    url = 'https://risenfromashes.us/info/serverinfo.php'
    html_content = request.urlopen(url).read().decode('utf-8')
    soup = BeautifulSoup(html_content, "lxml")
    players_table = list(soup.html.body.div.div.div.table.tr.children)[3]
    cuerpo = players_table.table.tbody
    players = list(map(lambda td: clean_html(str(td)), cuerpo.find_all('td')))
    return list(chunks(players, 4))


def is_playing(players, player):
    """Verify if the player is in list of players"""
    return len(list(filter(lambda p: p[0] == player, players))) > 0
