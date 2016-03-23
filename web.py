from slackbot.bot import respond_to
from slackbot.bot import listen_to
from slackbot.utils import download_file, create_tmp_file, till_white, till_end
from plugins.admin.perms import is_approved
import urllib
import urllib2
import re
import json, os

domain = "magfe.st"


def good_response(key):
    return "This page can be reached at http://%s/%s" % (domain, key)


def web_new_link(key, url):
    try:
            urllib2.urlopen(url)
            attempt = urllib2.urlopen("https://%s/newLink?%s" % (domain, urllib.urlencode({"key": key, "link":url})))
            return True
    except:
        return False


m_link = "\\bmake link\\b %s %s" % (till_white, till_end)
@respond_to(m_link, re.IGNORECASE)
#@listen_to(m_link, re.IGNORECASE, m_link_help)
def make_link(message, key, url):
    """
    make link (KEY) (URL) - makes a shortlink at the current domain with KEY
    """
    if is_approved(message, 'web'):
        url = url.strip('<> ')
        try:
            urllib2.urlopen(url)
            attempt = urllib2.urlopen("https://%s/newLink?%s" % (domain, urllib.urlencode({"key": key, "link":url})))
            message.send(attempt.read())
        except:
            message.send("Bad URL")

g_link = "\\bgen link\\b (.*)"
@respond_to(g_link, re.IGNORECASE)
#@listen_to(g_link, re.IGNORECASE, g_link_help)
def gen_link(message, url):
    """
    gen link (URL) - makes a shortlink at the current domain that has a randomly generated key
    """
    if is_approved(message, 'web'):
        url = url.strip('<> ')
        try:
            urllib2.urlopen(url)
            attempt = urllib2.urlopen("http://%s/genLink?%s" % (domain, urllib.urlencode({"link":url})))
            message.send(attempt.read())
        except:
            message.send("Bad URL")

master = "\\bmaster\\b"
@respond_to(master, re.IGNORECASE)
#@listen_to(master, re.IGNORECASE, master_help)
def master_links(message):
    """
    master - returns list of all current shortlinks available at %s
    """  % domain
    if is_approved(message, 'any'):
        try:
            attempt = urllib2.urlopen("http://%s/master" % (domain))
            message.upload_snippet(attempt.read().replace("<br>", "\n"), "Available Shortlinks")
        except:
            message.send("Unknown Error")

b = "\\bbadges$"
@respond_to(b, re.IGNORECASE)
#@listen_to(b, re.IGNORECASE)
def badges(message):
    if is_approved(message, "any"):
        try:
            attempt = urllib2.urlopen("https://prime.uber.magfest.org/uber/registration/stats")
            thing = (attempt.read())
            info = json.loads(thing)
            message.send("Badges Sold: %s\n Badges Remaining: %s" % (info['badges_sold'], info['remaining_badges']))
        except KeyError:
            message.send("Bad URL")
