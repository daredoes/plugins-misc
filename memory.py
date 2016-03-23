from slackbot.bot import respond_to
from slackbot.bot import listen_to
from slackbot.globals import attributes
from slackbot.utils import download_file, create_tmp_file, till_white, till_end
from plugins.admin.perms import is_approved
import re
import json, os
import random

try:
    db = attributes['db']
except KeyError:
    db = None



def memory_dict(term, thought):
    return {"key":term, "note":thought}

rem = "\\bremember\\b %s \\bis\\b %s" % (till_white, till_end)
#@listen_to(rem, re.IGNORECASE, rem_help)
@respond_to(rem, re.IGNORECASE)
def remember(message, key, note):
    """
    remember (KEY) is (VALUE) - sets the key to whatever is typed after 'is '
    """
    if is_approved(message, "any"):
        temp = note.split(" ")
        temp2 = ""
        for x in temp:
            if x[0] == "<" and x[len(x)-1] == ">":
                temp2 += " " + (x.strip("><"))
            else:
                temp2 += " " + (x)
        note = temp2.strip(" ")
        if db.mem.count({"key":key}) == 0:
            db.mem.insert_one(memory_dict(key, note))
            message.send("I'll be sure to remember that.")
        else:
            message.send("I already know something about %s" % key)

wha = "\\bwhat is\\b %s" % (till_white)
#@listen_to(wha, re.IGNORECASE, wha_help)
@respond_to(wha, re.IGNORECASE)
def what(message, key):
    """
    what is (KEY) - remembers the thing associated with KEY
    """
    if is_approved(message, "any"):
        if db.mem.count({"key":key}) != 0:
            thing = db.mem.find({"key":key})
            for x in thing:
                message.send(x['note'])
        else:
            message.send("I don't know what %s is" % key)

fer = '\\bforget what %s is' % till_white
#@listen_to(fer, re.IGNORECASE)
@respond_to(fer, re.IGNORECASE)
def forget(message, key):
    """
    forget what  (KEY) is - forgets the thing associated with KEY
    """
    if is_approved(message, "admin"):
        if db.mem.count({"key":key}) != 0:
            db.mem.delete_many({"key": key})
            message.send("I have forgotten what %s is" % key)
        else:
            message.send("I don't even know what %s is in the first place." % key)
