"""
Module: Players

Get all information related to players.
"""

from re import compile as comp, sub
import urllib.request as request

from bs4 import BeautifulSoup
import plotly.graph_objects as go
from more_itertools import unzip


def clean_html(raw_html):
    """Remove tags from `raw_html`"""
    output = sub(comp('<.*?>'), '', raw_html).strip()
    output = sub(comp('\^.'), '', output)
    return output


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

def generate_image():
    # import plotly
    # plotly.io.orca.config.executable = '/home/miguel/anaconda3/bin/orca'
    layout = go.Layout(autosize=True, margin={'l': 0, 'r': 0, 't': 0, 'b':0})
    players, score, ping, _ = unzip(get_players())
    players = list(players); score = list(score); ping = list(ping)
    height = len(list(players)) * 25 + 40
    fig = go.Figure(# columnwidth=[1,0.5,0.5],
                    layout=layout,
                    data = [go.Table(
                        columnwidth = [70,15,15],
                        header = dict(values=['<b>Player</b>',
                                              '<b>Score</b>',
                                              '<b>Ping</b>'],
                                      line_color='darkslategray',
                                      fill_color='lightskyblue',
                                      font_size=18,
                                      height=30,
                                      align=['left', 'center', 'center']),
                        cells = dict(values=[list(players),
                                             list(score),
                                             list(ping)],
                                     height=25,
                                     font_size=16,
                                     line_color='darkslategray',
                                     fill_color='lightcyan',
                                     align=['left', 'center', 'center'])
    )])
    fig.update_layout(width=400,height=height)
    loc = '/tmp/players.jpg'
    fig.write_image('/tmp/players.jpg', engine='kaleido')
    return loc
