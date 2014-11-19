# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import

from slugify import slugify
from google.appengine.ext import ndb
from google.appengine.api import channel

import utils
from listeners import push_event_created_notification, push_match_created_notification

match_created = utils.Event()
event_created = utils.Event()

match_created.append(push_match_created_notification)
event_created.append(push_event_created_notification)


class Match(ndb.Model):
    title = ndb.StringProperty()
    team_a = ndb.StringProperty()
    team_b = ndb.StringProperty()
    user = ndb.UserProperty()

    date = ndb.DateTimeProperty(auto_now_add=True)

    def put(self, *args, **kwargs):
        if not self.key:
            self.key = ndb.Key('Match', slugify(self.title))

        response = super(Match, self).put(*args, **kwargs)
        match_created(self)

        return response

    def to_dict(self, *args, **kwargs):
        d = super(Match, self).to_dict()
        d['slug'] = self.key.string_id()

        return d


class Event(ndb.Model):
    body = ndb.TextProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
    meta = ndb.JsonProperty()
    user = ndb.UserProperty()

    def put(self, *args, **kwargs):
        response =  super(Event, self).put(*args, **kwargs)
        event_created(self.key.parent().string_id(), self)

        return response


class Channel(ndb.Model):
    '''The list of currently active channels'''
    token = ndb.StringProperty()
    last_active = ndb.DateTimeProperty(auto_now_add=True)

    def send(self, data):
        channel.send_message(self.token, utils.to_json(data))

    @classmethod
    def create_user_channel(cls, user):
        token = channel.create_channel(user.user_id())
        c = cls(key=ndb.Key('Channel', user.user_id()), token=token).put()

        return token, c
