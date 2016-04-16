from slackbot.bot import respond_to
from slackbot.bot import listen_to
from slackbot.globals import attributes
from slackbot.utils import till_white, till_end
from plugins.admin.perms import is_approved
import urbandict
import re

try:
    db = attributes['db']
except KeyError:
    db = None


@respond_to("define %s" % till_end, re.IGNORECASE)
def urban_response(message, term):
    if is_approved(message, "any"):
        terms = urbandict.define(term)
        for x in terms:
            if x['example'] == '' and len(terms) == 1:
                message.send("No definitions found for %s" % term)
                break
            temp = "Definition: %s Examples: %s" % (x['def'], x['example'])
            message.upload_snippet(temp, x['word'].strip("\n "))