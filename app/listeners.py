# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import

import pusher
from . import app

p_client = pusher.Pusher(
    app_id=app.config['PUSHER_APP'],
    key=app.config['PUSHER_KEY'],
    secret=app.config['PUSHER_SECRET'])


def push_event_created_notification(event, **kwargs):
    p_client[event['slug']].trigger('new-event', event)


def push_match_created_notification(match, **kwargs):
    p_client['feeds'].trigger('new-feed', match)
