from slackbot.bot import respond_to
from slackbot.bot import listen_to
from slackbot.utils import download_file, create_tmp_file, till_white, till_end
from slackbot.plugins.admin.perms import is_approved
import re
import random

r_d = "\\broll\\b d%s" % till_white
#@listen_to(r_d, re.IGNORECASE)
@respond_to(r_d, re.IGNORECASE)
def roll(message, sides):
    if is_approved(message, "any"):
        try:
            sides = int(sides)
            message.send("You rolled %d" % random.randint(1, sides))
        except ValueError:
            message.send("Not a proper integer")

f_c = '\\bflip coin\\b'
#@listen_to(f_c, re.IGNORECASE)
@respond_to(f_c, re.IGNORECASE)
def flip_coin(message):
    if is_approved(message, "any"):
        if random.random() % 2 == 0:
            message.send("Heads")
        else:
            message.send("Tails")
