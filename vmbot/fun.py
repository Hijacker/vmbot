# coding: utf-8

import random
import re
import cgi
import urllib

import requests
from bs4 import BeautifulSoup

from .botcmd import botcmd
from .helpers.files import EMOTES

# 8ball answers like the original, as per http://en.wikipedia.org/wiki/Magic_8-Ball
EBALL_ANSWERS = (
    "It is certain",
    "It is decidedly so",
    "Without a doubt",
    "Yes definitely",
    "You may rely on it",
    "As I see it, yes",
    "Most likely",
    "Outlook good",
    "Yes",
    "Signs point to yes",
    "Reply hazy try again",
    "Ask again later",
    "Better not tell you now",
    "Cannot predict now",
    "Concentrate and ask again",
    "Don't count on it",
    "My reply is no",
    "My sources say no",
    "Outlook not so good",
    "Very doubtful"
)

FISHISMS = (
    "~The Python Way!~",
    "HOOOOOOOOOOOOOOOOOOOOOOO! SWISH!",
    "DIVERGENT ZONES!",
    "BONUSSCHWEIN! BONUSSCHWEIN!"
)

PIMPISMS = (
    "eabod",
    "why do you hate black people?",
    "i want a bucket full of money covered rainbows",
    "bundle of sticks",
    "that went over like a jerrys kids rodeo with live bulls"
)

ARELEISMS = (
    "PzbjWI3EhyI",
    "5R8At-Qno_o",
    "MZwXoDyj9Vc",
    "So9LshyaHd0",
    "sW4JRSzPJQo",
    "UepAzio1eyU",
    "aneUrHBRyhg",
    "9XHqg7mTizE",
    "gtM9xD-Ky7E",
    "ZTidn2dBYbY"
)

NICKISMS = (
    "D{}d!",
    "But d{}d!",
    "Come on d{}d...",
    "Oh d{}d",
    "D{}d, never go full retart!"
)

KAIRKISMS = (
    "thanks for filling this out.",
    "voting on your application to join VM is over, and you have passed.",
    "congratulations, you passed the security check.",
    "I regret to tell you that your application to join VM has been rejected.",
    "thank you for your interest in VM, and I wish you luck in your future endeavours in Eve.",
    "in 48h your membership of Valar Morghulis. will be terminated.",
    "you've got to improve, or I'll be sending out more kick notices, and I hate doing that.",
    "you get a cavity search, your friends get a cavity search, EVERYBODY gets a cavity search!"
)

DARIUSISMS = (
    "Baby",
)

SCOTTISMS = (
    "would you like to buy a rose?",
    "Israel has a right to defend itself."
)

JOKERISMS = (
    "dont be a retard",
    "dont ruin our zkb efficiency",
    "urbad"
)


class Say(object):
    @botcmd
    def fishsay(self, mess, args):
        """Fishy wisdom"""
        return random.choice(FISHISMS)

    @botcmd
    def pimpsay(self, mess, args):
        """Like fishsay but blacker"""
        if args:
            return "{} {}".format(args, random.choice(PIMPISMS))
        else:
            return random.choice(PIMPISMS)

    @botcmd
    def arelesay(self, mess, args):
        """Like fishsay but more fuckey"""
        return "https://youtu.be/{}".format(random.choice(ARELEISMS))

    @botcmd
    def nicksay(self, mess, args):
        """Like fishsay but pubbietasticer"""
        return random.choice(NICKISMS).format('0' * int(2 + random.expovariate(.25)))

    @botcmd
    def chasesay(self, mess, args):
        """Please"""
        sender = args.strip() or self.get_sender_username(mess)
        return "{}, would you PLEASE".format(sender)

    @botcmd
    def kairksay(self, mess, args):
        """Like fishsay but more Kafkaesque"""
        sender = args.strip() or self.get_sender_username(mess)
        return "{}, {} -Kairk".format(sender, random.choice(KAIRKISMS))

    @botcmd
    def dariussay(self, mess, args):
        """Like fishsay but bordering on weird"""
        sender = args.strip() or self.get_sender_username(mess)
        return "{}, {}".format(sender, random.choice(DARIUSISMS))

    @botcmd
    def scottsay(self, mess, args):
        """Like fishsay but coming from Israel"""
        if args:
            return "{}, {}".format(args, random.choice(SCOTTISMS))
        else:
            return random.choice(SCOTTISMS)

    @botcmd
    def eksay(self, mess, args):
        """Like fishsay but more dead"""
        sender = args.strip() or self.get_sender_username(mess)
        return ":rip: {}".format(sender)

    @botcmd
    def jokersay(self, mess, args):
        """Like fishsay but german"""
        if args:
            return "{} {}".format(args, random.choice(JOKERISMS))
        else:
            return random.choice(JOKERISMS)

    @botcmd(name="8ball")
    def bot_8ball(self, mess, args):
        """<question> - Provides insight into the future"""
        if not args:
            return "You will need to provide a question for me to answer"
        else:
            return random.choice(EBALL_ANSWERS)

    @botcmd
    def sayhi(self, mess, args):
        """[name] - Says hi to you or name if provided"""
        sender = args.strip() or self.get_sender_username(mess)
        return "Hi {}!".format(sender)


class Fun(object):
    @botcmd
    def rtd(self, mess, args):
        """Like a box of chocolates, you never know what you're gonna get"""
        with open(EMOTES, 'r') as emotes_file:
            emotes = emotes_file.read().splitlines()

        while not emotes.pop(0) == "[default]":
            pass

        return random.choice(emotes).split()[-1]

    @botcmd
    def rtq(self, mess, args):
        """Like a box of chocolates, but without emotes this time"""
        try:
            r = requests.get("http://bash.org/?random", timeout=5)
        except requests.exceptions.RequestException as e:
            return "Error while connecting to http://bash.org: {}".format(e)
        soup = BeautifulSoup(r.text, "html.parser")

        valid_ids = {int(link['href'][1:]) for link
                     in soup.find_all("a", title="Permanent link to this quote.")}

        if not valid_ids:
            return "Failed to load any quotes from http://bash.org/?random"

        quote_id = random.choice(tuple(valid_ids))
        quote_url = "http://bash.org/?{}".format(quote_id)

        try:
            r = requests.get(quote_url, timeout=3)
        except requests.exceptions.RequestException as e:
            return "Error while connecting to http://bash.org: {}".format(e)
        soup = BeautifulSoup(r.text, "html.parser")

        try:
            quote = soup.find("p", class_="qt").text
        except AttributeError:
            return "Failed to load quote #{} from {}".format(quote_id, quote_url)

        return u"{}\n{}".format(quote_url, quote)

    @botcmd
    def rtxkcd(self, mess, args):
        """Like a box of chocolates, but with xkcds"""
        try:
            res = requests.get("https://xkcd.com/info.0.json", timeout=3).json()
        except requests.exceptions.RequestException as e:
            return "Error while connecting to https://xkcd.com: {}".format(e)
        except ValueError:
            return "Error while parsing response from https://xkcd.com"

        comic_id = random.randint(1, res['num'])
        comic_url = "https://xkcd.com/{}/".format(comic_id)

        try:
            comic = requests.get("{}info.0.json".format(comic_url), timeout=3).json()
        except requests.exceptions.RequestException as e:
            return "Error while connecting to https://xkcd.com: {}".format(e)
        except ValueError:
            return "Failed to load xkcd #{} from {}".format(comic_id, comic_url)

        return "<b>{}</b> (<i>{}/{}/{}</i>): {}".format(comic['safe_title'], comic['year'],
                                                        comic['month'], comic['day'], comic_url)

    @botcmd
    def rtud(self, mess, args):
        """Like a box of chocolates, but with loads of pubbie talk"""
        return self.urban(mess, "")

    @botcmd
    def urban(self, mess, args):
        """[word] - Displays Urban Dictionary's definition of word or, if missing, a random word"""
        url = "http://api.urbandictionary.com/v0/"
        url += "random" if not args else "define"
        params = None if not args else {'term': args}

        try:
            res = requests.get(url, params=params, timeout=3).json()
        except requests.exceptions.RequestException as e:
            return "Error while connecting to https://www.urbandictionary.com: {}".format(e)
        except ValueError:
            return "Error while parsing response from https://www.urbandictionary.com"

        if not res['list']:
            return 'Failed to find any definitions for "{}"'.format(args)

        # Create a list of definitions with positive (>= 0) rating numbers
        choices = [(desc, desc['thumbs_up'] - desc['thumbs_down']) for desc in res['list']]
        min_rating = min(desc[1] for desc in choices)
        if min_rating < 0:
            abs_min = abs(min_rating)
            choices = [(desc[0], desc[1] + abs_min) for desc in choices]

        # Select a random definition using rating as weight
        rand = random.uniform(0, sum(choice[1] for choice in choices))
        entry = None

        for desc, weight in choices:
            rand -= weight
            if rand <= 0:
                entry = desc
                break

        def urban_link(match):
            return '<a href="https://www.urbandictionary.com/define.php?term={}">{}</a>'.format(
                urllib.quote_plus(match.group(1)), match.group(1)
            )

        desc = cgi.escape(entry['definition'])
        desc = re.sub("((?:\r|\n|\r\n)+)", "<br />", desc).rstrip("<br />")
        desc = re.sub("\[([\S ]+?)\]", urban_link, desc)

        desc = u"<b>{}</b> by <i>{}</i> rated {:+}: {}<br />{}".format(
            entry['word'], entry['author'], entry['thumbs_up'] - entry['thumbs_down'],
            entry['permalink'], desc
        )

        if 'tags' in res and res['tags']:
            desc += "<br />{}".format(' '.join("#{}".format(tag) for tag in res['tags']))

        return desc


class Chains(object):
    @botcmd(hidden=True, name="every")
    def bot_every(self, mess, args):
        """Every lion except for at most one"""
        if not args and random.randint(1, 5) == 1:
            return "lion"

    @botcmd(hidden=True, name="lion")
    def bot_lion(self, mess, args):
        """Every lion except for at most one"""
        if not args and random.randint(1, 5) == 1:
            return "except"

    @botcmd(hidden=True, name="except")
    def bot_except(self, mess, args):
        """Every lion except for at most one"""
        if not args and random.randint(1, 5) == 1:
            return "for"

    @botcmd(hidden=True, name="for")
    def bot_for(self, mess, args):
        """Every lion except for at most one"""
        if not args and random.randint(1, 5) == 1:
            return "at"

    @botcmd(hidden=True, name="at")
    def bot_at(self, mess, args):
        """Every lion except for at most one"""
        if not args and random.randint(1, 5) == 1:
            return "most"

    @botcmd(hidden=True, name="most")
    def bot_most(self, mess, args):
        """Every lion except for at most one"""
        if not args and random.randint(1, 5) == 1:
            return "one"

    @botcmd(hidden=True, name="one")
    def bot_one(self, mess, args):
        """Every lion except for at most one"""
        if not args and random.randint(1, 5) == 1:
            return ":bravo:"

    @botcmd(hidden=True, name='z')
    def bot_z(self, mess, args):
        """z0r"""
        if not args and random.randint(1, 3) == 1:
            return '0'

    @botcmd(hidden=True, name='0')
    def bot_0(self, mess, args):
        """z0r"""
        if not args and random.randint(1, 3) == 1:
            return 'r'

    @botcmd(hidden=True, name='r')
    def bot_r(self, mess, args):
        """z0r"""
        if not args and random.randint(1, 3) == 1:
            return 'z'
