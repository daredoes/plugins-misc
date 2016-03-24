# -*- coding: utf-8 -*-
from slackbot.bot import respond_to
from slackbot.bot import listen_to
from slackbot.manager import PluginsManager
from plugins.admin.perms import is_approved
from slackbot.utils import till_white, till_end, to_utf8
import re
import bs4, requests

@respond_to("badges gx4$", re.IGNORECASE)
def gx_badges(message):
    res = requests.get('https://www.eventbrite.com/e/gaymerx-year-four-tickets-20100576365')
    res.raise_for_status()
    nss = bs4.BeautifulSoup(res.text)
    tickets = {}
    ticket_name = ""
    for x in nss.select("td[itemprop]"):
        if x.attrs['itemprop'] == 'name':
            ticket_name = x.contents[2].strip(" \n").partition("\n")[0]
            tickets[ticket_name] = ""
        if x.attrs['itemprop'] == 'inventoryLevel':
            ticket_count = x.getText().partition("= '")[2].partition("'")[0]
            tickets[ticket_name] = ticket_count
    t_string = ""
    for x in tickets:
        t_string += "%s - %s\n" % (x, tickets[x])
    message.upload_snippet(t_string, "GX4 Tickets Remaining")
