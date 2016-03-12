# -*- coding: utf-8 -*-
from slackbot.bot import respond_to
from slackbot.bot import listen_to
from slackbot.dispatcher import PluginsManager
from slackbot.plugins.admin.perms import is_approved
from slackbot.utils import till_white, till_end, to_utf8
import re
from six import iteritems
import random

answer_key = ""
insults = [
    "Hey %s, you're dumb."
]

domain = "magfe.st"
responses = []
noises = []

orders = {"66":"It shall be done, my liege.", "delta alfa romeo echo":"butts.",
          "overtaker": "Soon I will consume MAGBot whole."}


def reply_to_tuple(trigger, response, perm, halp=""):
    if halp == "":
        halp = "Include '%s' in any command to trigger a response" % trigger.replace("\\b", "").replace(till_white, "(until whitespace)").replace(till_end, "(until end of line)")
    return (trigger, response, perm, halp)


def random_ha():
    return str("ha" * random.randint(3,10))
orders['giggles'] = random_ha

def field_dict(title, value):
    return {"title": title, "value": value}


def user_dict(username, id, permissions=""):
    return {"user": username, "id": id, 'permissions': permissions}


def recur(trigger, response, perm, halp):
    #@listen_to(trigger, re.IGNORECASE, halp)
    @respond_to(trigger, re.IGNORECASE, halp)
    def basic_reply(message):
        if is_approved(message, perm):
            if isinstance(response, str):
                message.send(response)
            else:
                message.send(response())

def ears(trigger, response, perm, halp):
    @listen_to(trigger, re.IGNORECASE, halp)
    #@respond_to(trigger, re.IGNORECASE, halp)
    def basic_reply(message):
        if is_approved(message, perm):
            if isinstance(response, str):
                message.send(response)
            else:
                message.send(response())


responses.append(reply_to_tuple("\\bbad\\b", "I'm sorry! Please forgive me!", "any"))
responses.append(reply_to_tuple("\\bbehave\\b", "I will do my *best*!", "any"))
responses.append(reply_to_tuple('\\blaugh\\b', random_ha, "any"))
responses.append(reply_to_tuple('\\bleave\\b', "You first!", "any"))
responses.append(reply_to_tuple('\\bpet\\b', "What a _kind_ gesture.", "any"))
responses.append(reply_to_tuple('\\bbite\\b', "*BITES BACK!*", "any"))
responses.append(reply_to_tuple('\\bactivate skynet\\b', "_Skynet_ *ACTIVATED*", "any"))
responses.append(reply_to_tuple('\\blove me\\b',"How about... *no.*", "any"))
noises.append(reply_to_tuple('\\b420\\b', "Drugs are *bad*. Stay in school.", "any"))

for x in responses:
    recur(x[0], x[1], x[2], x[3])
for x in noises:
    ears(x[0], x[1], x[2], x[3])


woagh = '\\bwo+?a+?g+?h+?\\b'
@listen_to(woagh, re.IGNORECASE, halp="wo(repeatable)a(repeatable)g(repeatable)h(repeatable)")
@respond_to(woagh, re.IGNORECASE, halp="wo(repeatable)a(repeatable)g(repeatable)h(repeatable)")
def woooaaagh(message):
    if is_approved(message, "any"):
        message.react("colossus")
        message.send("*WOAAAAAAAGGHHHH!*\nhttps://pbs.twimg.com/media/B8JvTeMIIAAbXYA.jpg:large")

help_str = '\\bhelp\\b'
command_str= '\\bcommands\\b'
@listen_to(help_str, re.IGNORECASE, "help - pulls up the available commands")
@listen_to(command_str, re.IGNORECASE, "commands - pulls up the available commands")
def help_commands2(message):
    if is_approved(message, "any"):
        coms = PluginsManager.commands['listen_to']
        default_reply = [
            'You can ask me one of the following questions:\n',
        ]
        default_reply += ['{0} {1}'.format(p[1]
                                                   , v.__doc__ or "")
                          for p, v in iteritems(coms)]

        default_reply = '\n'.join(to_utf8(default_reply))
        message.upload_snippet(str(default_reply), "Commands")

@respond_to(help_str, re.IGNORECASE, "help - pulls up the available commands")
@respond_to(command_str, re.IGNORECASE, "commands - pulls up the available commands")
def help_commands(message):
    if is_approved(message, "any"):
        coms = PluginsManager.commands['respond_to']
        default_reply = [
            'You can ask me one of the following questions:\n',
        ]
        default_reply += ['{0} {1}'.format(p[1]
                                                   , v.__doc__ or "")
                          for p, v in iteritems(coms)]

        default_reply = '\n'.join(to_utf8(default_reply))
        message.upload_snippet(str(default_reply), "Commands")


order_sent = "\\bexecute order\\b (.*$)"
@listen_to(order_sent, re.IGNORECASE, halp="Execute Order (command)")
@respond_to(order_sent, re.IGNORECASE, halp="Execute Order (command)")
def execute_orders(message, order):
    if is_approved(message, "any"):
        if order in orders.keys():
            if isinstance(orders[order], str):
                message.send(orders[order])
            else:
                message.send(orders[order]())
