from slackbot.bot import respond_to
from slackbot.bot import listen_to
from slackbot.globals import attributes
from slackbot.utils import till_white, till_end
from plugins.admin.perms import is_approved
import re

try:
    db = attributes['db']
except KeyError:
    db = None

try:
    botname = attributes['bot_name']
except KeyError:
    botname = None


def who_loves_dict(the_love, the_lovers):
    if isinstance(the_lovers, list):
        temp = ""
        for x in the_lovers:
            temp += x + ","
        temp = temp.strip(", ")
        return {"love": the_love, "lovers": temp}
    else:
        return {"love": the_love, "lovers": the_lovers}

who_loves = "\\bwho loves\\b %s$" % till_end
@listen_to(who_loves, re.IGNORECASE)
@respond_to(who_loves, re.IGNORECASE)
def who_could_love(message, the_love):
    """
    who loves (subject) - returns all users who love such a subject
    """
    the_love = the_love.strip("@.,?!")
    if is_approved(message, "any"):
        if db.loves.count({"love":the_love}) != 0:
            for x in db.loves.find({"love":the_love}):
                temp = ""
                for lover in x['lovers'].split(","):
                    temp += "%s *loves* %s\n" % (lover, the_love)
                message.send(temp)
        else:
            message.send("Nobody loves %s..." % the_love)

forget_love = "\\bforget who loves\\b %s" % till_end
#@listen_to(forget_love, re.IGNORECASE)
@respond_to(forget_love, re.IGNORECASE)
def forget_loving(message, the_love):
    """
    forget who loves (subject) - forgets everyone who loves that subject
    """
    if is_approved(message, "admin"):
        db.loves.delete_many({"love":the_love})
        message.send("I forgot who loves %s" % the_love)

they_love = "%s \\bloves\\b %s" % (till_white, till_end)
ther_love = "%s \\blove\\b %s" % (till_white, till_end)
@listen_to(they_love, re.IGNORECASE)
@respond_to(they_love, re.IGNORECASE)
@listen_to(ther_love, re.IGNORECASE)
@respond_to(ther_love, re.IGNORECASE)
def they_could_love(message, lovers, the_love):
    """
    (user) love[s] (subject) - has %s remember who loves (subject)
    """ % botname
    the_love = the_love.strip("?,!.@")
    lovers = lovers.strip("$<.>'")
    if lovers.lower() == "i":
        lovers = message.sent_by()
    if lovers == "who":
        pass
    elif the_love == "me":
        pass
    else:
        if is_approved(message, "any"):
            temp = ""
            if "," in lovers:
                        lovers = lovers.split(",")
                        for love in lovers:
                            if love[0] == "_":
                                temp += love[1:] + ","
                            elif message.name_to_id(love.strip(" ")) != "Not Found":
                                temp += love.strip(" ") + ","
                        temp = temp.strip(" ,")
            #db.loves.delete_many({})
            else:
                    if lovers[0] == "_":
                        temp = lovers[1:]
                    elif message.name_to_id(lovers) != "Not Found":
                        temp = lovers
                    else:
                        message.send("That's not a person in this slack!")
                        return

            if db.loves.count({"love":the_love}) == 0:
                db.loves.insert_one(who_loves_dict(the_love, temp))
                message.send("That's great to know!")
            else:
                thing = db.loves.find({"love":the_love})
                for x in thing:
                    if "," in temp:
                        doTemp = ""
                        for y in temp.split(','):

                            if y.strip(" ") not in x['lovers']:
                                doTemp += y.strip(" ") + ","
                            else:
                                message.send("%s already loves %s" % (y, the_love))
                        temp = doTemp.strip(", ")
                    if temp not in x['lovers']:
                        db.loves.update_one({"love":the_love}, {"$set":{
                            "lovers": x['lovers'] + "," + temp
                            }})
                        message.send("That's great to know!")
                    else:
                        message.send("I already know that %s loves %s" % (temp, the_love))
