# coding: utf-8

from __future__ import absolute_import, division, unicode_literals, print_function

from datetime import datetime, timedelta
import re
import json

import requests

from ..helpers.exceptions import NoCacheError
from ..helpers import database as db


def parse_http_cache(headers):
    """Parse HTTP caching headers."""
    if 'Cache-Control' not in headers:
        raise NoCacheError

    cache_control = headers['Cache-Control'].lower()
    if "no-cache" in cache_control or "no-store" in cache_control:
        raise NoCacheError

    timer = re.search(r"max-age=(\d+)", cache_control, re.IGNORECASE)
    if timer is not None:
        return datetime.utcnow() + timedelta(seconds=int(timer.group(1)))
    elif 'Expires' in headers:
        return datetime.strptime(headers['Expires'], "%a, %d %b %Y %H:%M:%S %Z")
    else:
        raise NoCacheError


class BaseCacheObject(db.Model):
    """Cache arbitrary data."""
    __tablename__ = "cache"

    key = db.Column(db.String, nullable=False, primary_key=True)
    value = db.Column(db.LargeBinary, nullable=False)
    expiry = db.Column(db.DateTime, nullable=False)

    def __init__(self, key, value, expiry):
        self.key = key
        self.value = value
        self.expiry = expiry

    def save(self, session):
        """Save cache object to the database."""
        session.merge(self)
        session.commit()

    @classmethod
    def get(cls, session, key):
        """Load cached data from the database."""
        cls.clear(session)

        return session.query(cls.value).filter_by(key=key).scalar()

    @classmethod
    def clear(cls, session):
        """Delete outdated cache objects from the database."""
        session.query(cls).filter(cls.expiry < datetime.utcnow()).delete()
        session.commit()


class HTTPCacheObject(BaseCacheObject):
    """Cache an HTTP response using URL, parameters, body, and headers as key."""

    def __init__(self, url, doc, expiry=None, params=None, data=None, headers=None):
        url += json.dumps(params) if params else ""
        url += json.dumps(data) if data else ""
        url += json.dumps(headers) if headers else ""
        expiry = expiry or datetime.utcnow() + timedelta(hours=1)
        super(HTTPCacheObject, self).__init__(url, doc, expiry)

    @classmethod
    def get(cls, session, url, params=None, data=None, headers=None):
        """Load cached HTTP response from the database."""
        url += json.dumps(params) if params else ""
        url += json.dumps(data) if data else ""
        url += json.dumps(headers) if headers else ""
        return super(HTTPCacheObject, cls).get(session, url)


class ESICacheObject(HTTPCacheObject):
    """Cache an ESI response."""

    def __init__(self, url, r, expiry=None, params=None, data=None, headers=None):
        doc = json.dumps(dict(r.headers)) + b'\0' + r.content
        super(ESICacheObject, self).__init__(url, doc, expiry, params, data, headers)

    @classmethod
    def get(cls, session, url, params=None, data=None, headers=None):
        """Load cached ESI response from the database."""
        doc = super(ESICacheObject, cls).get(session, url, params, data, headers)
        if doc is None:
            return None

        r = requests.Response()
        head, r._content = doc.split(b'\0', 1)
        r.headers.update(json.loads(head))
        return r
