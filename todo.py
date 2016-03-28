from slackbot.bot import respond_to
from slackbot.bot import listen_to
from slackbot.globals import attributes
from slackbot.utils import download_file, create_tmp_file, till_white, till_end
from plugins.admin.perms import is_approved
import re

try:
    db = attributes['db']
except KeyError:
    db = None


"""
The Goal is to make an individual to-do list for every person.
"""

def to_do_dict(owner):
    return {"owner":owner, "items":""}

t_list = "\\bto-do list\\b"
#@listen_to(t_list, re.IGNORECASE)
@respond_to(t_list, re.IGNORECASE)
def list_to_do_items(message):
    if is_approved(message, "any"):
        o_d = {"owner":message.sent_by()}
        if db.todo.count(o_d) == 0:
            message.send("You don't have a to-do list.\nAdd one with 'to-do add (text)'")
        else:
            temp = ""
            count = 1
            for x in db.todo.find(o_d):
                for y in x['items'].split(","):
                    temp += "%d. %s\n" % (count, y)
                    count += 1
                message.upload_snippet(temp, "To-Do List of %s" % message.sent_by())

t_add = "\\bto-do add\\b %s" % till_end
#@listen_to(t_add, re.IGNORECASE, t_add_help)
@respond_to(t_add, re.IGNORECASE)
def add_to_do_items(message, items):
    """to-do add (text) - Separate items with commas"""
    temp = items.split(",")
    items = ""
    for x in temp:
        items += x.strip(" ") + ","
    items.strip(",")
    if is_approved(message, "any"):
        try:
            o_d = {"owner":message.sent_by()}
            if db.todo.count(o_d) == 0:
                db.todo.insert_one(to_do_dict(message.sent_by()))
            for x in db.todo.find(o_d):
                db.todo.update_one(o_d, {"$set":{"items": str(x['items'] + "," + items).strip(",")}})
                message.send("To-do list updated.")
        except UnicodeDecodeError:
            message.send("Uhhhh is that in Unicode?")

t_remove = "\\bto-do remove\\b %s" % till_white
#@listen_to(t_remove, re.IGNORECASE, t_remove_help)
@respond_to(t_remove, re.IGNORECASE)
def remove_to_do_item(message, item):
    """to-do remove (#) - Removes the task with the associated digit"""
    if is_approved(message, "any"):
        o_d = {"owner":message.sent_by()}
        if db.todo.count(o_d) == 0:
            message.send("You don't have a to-do list.\nAdd one with 'to-do add (text)'")
        else:
            for x in db.todo.find(o_d):
                try:
                    test = x['items'].split(',')
                    rem = test[int(item)-1]
                    at_rem = x['items'].partition(rem)
                    new_items = "%s%s" % (at_rem[0],(at_rem[2]))
                    new_items = new_items.replace(",,", ",").strip(",")
                    if new_items != "":
                        db.todo.update_one(o_d, {"$set":{
                            "items": new_items
                        }})
                    else:
                        db.todo.delete_many(o_d)
                    message.send("Task '%s' removed" % rem)
                except:
                    message.send("That wasn't a number")

t_done = "\\bto-do finish\\b %s" % till_white
#@listen_to(t_done, re.IGNORECASE, t_done_help)
@respond_to(t_done, re.IGNORECASE)
def finish_to_do_item(message, item):
    """to-do finish (#) - Marks the task with the associated digit with DONE"""
    if is_approved(message, "any"):
        o_d = {"owner":message.sent_by()}
        if db.todo.count(o_d) == 0:
            message.send("You don't have a to-do list.\nAdd one with 'to-do add (text)'")
        else:
            for x in db.todo.find(o_d):
                try:
                    rem = x['items'].split(',')[int(item)-1]
                    at_rem = x['items'].partition(rem)
                    new_items = "%sDONE-%s" % (at_rem[0],(at_rem[1] + at_rem[2]))
                    if "DONE-" not in rem[0-5]:
                        db.todo.update_one(o_d, {"$set":{
                            "items": new_items
                        }})
                    message.send("Task '%s' marked as complete" % rem)
                except IndexError:
                    message.send("That task wasn't found")
