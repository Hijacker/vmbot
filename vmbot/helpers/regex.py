# coding: utf-8

from __future__ import absolute_import, division, unicode_literals, print_function

import re

# Pubbie talk regex parts
PUBBIETALK = (
    "sup",
    "dank",
    "o7",
    "o\/",
    "m8",
    "retart",
    "rekt",
    "toon(?:ies)?",
    "iskies",
    "(?:thann?|chimm?|nidd?)(?:y|ies)",
    "yolo",
    "swag",
    "wewlad",
    "2?stronk",
    "linky"
)

PUBBIE_REGEX = re.compile(r"\b(?:{})\b".format('|'.join(PUBBIETALK)), re.IGNORECASE)

ZKB_REGEX = re.compile("https?://zkillboard\.com/kill/(-?\d+)/?", re.IGNORECASE)

TIME_OFFSET_REGEX = re.compile(r"(?:(\d+)d)?(?:(\d+)h)?(?:(\d+)m)?\b", re.IGNORECASE)
